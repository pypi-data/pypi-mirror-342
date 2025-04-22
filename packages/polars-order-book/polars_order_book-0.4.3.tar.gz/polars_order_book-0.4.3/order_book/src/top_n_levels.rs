use std::fmt::Debug;

use order_book_core::price_level::{self, PriceLevel, QuantityLike};
use tracing::{debug, instrument};

/// Trait for book side operations with top N tracking.
///
/// TopNLevels is an array of Option<PriceLevel> with length N.
/// with None representing that there are less than N levels in
/// total. The array is sorted from best to worst price level.
/// The array is updated on every add_qty and delete_qty operation.
pub struct NLevels<Price: price_level::Price, Qty: QuantityLike, const N: usize> {
    pub levels: [Option<PriceLevel<Price, Qty>>; N],
    pub worst_price: Option<Price>,
}

impl<Price: price_level::Price, Qty: QuantityLike, const N: usize> Debug
    for NLevels<Price, Qty, N>
{
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}-Levels {{ levels: {:?}, worst: {:?} }}",
            N, self.levels, self.worst_price
        )
    }
}
impl<Price: price_level::Price, Qty: QuantityLike, const N: usize> NLevels<Price, Qty, N> {
    pub(crate) fn new() -> Self {
        Self::default()
    }
}

impl<Price: price_level::Price, Qty: QuantityLike, const N: usize> Default
    for NLevels<Price, Qty, N>
{
    fn default() -> Self {
        assert!(N > 0, "TopNLevels: N must be greater than 0");
        NLevels {
            levels: core::array::from_fn(|_| None), // Avoids PriceLevel requiring Copy trait
            worst_price: None,
        }
    }
}
impl<Price: price_level::Price, Qty: QuantityLike, const N: usize> NLevels<Price, Qty, N> {
    pub fn best_level(&self) -> Option<&PriceLevel<Price, Qty>> {
        self.levels[0].as_ref()
    }
    pub fn best_price(&self) -> Option<Price> {
        self.best_level().map(|level| level.price)
    }

    pub fn best_price_qty(&self) -> Option<Qty> {
        self.best_level().map(|level| level.qty)
    }
}

/// General heuristic: iterate prices from best to worst, because order books tend to be updated more
/// frequently on top of book than lower levels. Also assuming that N is likely to be small,
/// e.g. less than 10, so that something like a binary search is not magnitudes better
/// in the worst case.
/// TODO: X_sort methods could be expressed more generally, i.e. without mentioning Price and Qty.
impl<Price: price_level::Price, Qty: QuantityLike, const N: usize> NLevels<Price, Qty, N> {
    /// Insert a new level into the *already sorted* levels array,
    /// and re-order so that the array remains sorted. This function
    /// is for arrays sorted from largest to smallest, with Nones
    /// at the right.
    pub fn try_insert_sort(&mut self, new_level: PriceLevel<Price, Qty>) {
        if let Some(worst_price) = self.worst_price {
            if worst_price > new_level.price {
                debug!("price below worst tracked price, ignoring");
                return;
            }
        }
        self.insert_sort(new_level);
    }

    #[instrument]
    pub fn insert_sort(&mut self, new_level: PriceLevel<Price, Qty>) {
        // TODO - investigate optimisation: could be faster to insert at the last non-None entry, so we can
        // rotate a shorter slice.
        let new_price = new_level.price;
        self.levels[N - 1] = Some(new_level);
        let mut insertion_point = None;
        for (i, entry) in self.levels[..N - 1].iter().enumerate() {
            match entry {
                Some(level) if new_price < level.price => {}
                _ => {
                    insertion_point = Some(i);
                    break;
                }
            }
        }
        if let Some(insertion_point) = insertion_point {
            debug!("Insertion point: {}", insertion_point);
            self.levels[insertion_point..].rotate_right(1);
        }
        self.worst_price = self.levels[N - 1].map(|level| level.price);
    }

    /// Replace an existing level with a new level, and re-order so that the array remains sorted.
    /// Assumes that the array is *already sorted*, and ordered from largest to smallest, with Nones
    /// at the right. Also assumes that price_to_replace is in the array.
    #[instrument]
    pub fn replace_sort(
        &mut self,
        price_to_replace: Price,
        new_level: Option<PriceLevel<Price, Qty>>,
    ) {
        for (i, entry) in self.levels.iter_mut().enumerate() {
            if let Some(level) = entry {
                if level.price == price_to_replace {
                    debug!("Found level to replace {:?}", level);
                    self.worst_price = new_level.map(|level| level.price);
                    *entry = new_level;
                    // TODO - optimisation: we rotate more entries than necessary in the case
                    // where some entries are None. Could be faster to avoid this.
                    self.levels[i..].rotate_left(1);
                    return;
                }
            }
        }
        debug!("Iterated through levels but did not replace any");
    }

    #[instrument]
    pub fn update_qty(&mut self, price: Price, new_qty: Qty) {
        // TODO - optimisation: could check against worst price to avoid iterating over all levels
        for level in self.levels.iter_mut().flatten() {
            if level.price == price {
                debug!("Updating qty for level: {:?}", level);
                level.qty = new_qty;
                return;
            }
        }
        debug!("Iterated through levels but did not update any");
    }
}

#[cfg(test)]
mod tests {
    use order_book_core::price_level::{AskPrice, BidPrice, Price};

    use super::*;

    #[test]
    fn test_n_levels_constructor() {
        let n_levels: NLevels<BidPrice<i32>, i32, 5> = NLevels::default();
        assert_eq!(n_levels.levels.len(), 5);
        assert!(n_levels.levels.iter().all(|level| level.is_none()));
        assert_eq!(n_levels.worst_price, None);
    }

    #[test]
    fn test_insert() {
        let mut n_levels = NLevels::<BidPrice<i32>, i32, 5>::default();
        let level = PriceLevel::new(1.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels[0], Some(level));

        let mut n_levels = NLevels::<AskPrice<i32>, i32, 5>::default();
        let level = PriceLevel::new(1.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels[0], Some(level));
    }

    fn get_price_levels<Px: Price + From<i32>>(
        prices: [i32; 5],
    ) -> [Option<PriceLevel<Px, i32>>; 5] {
        prices.map(|price| Some(PriceLevel::new(price.into())))
    }

    fn get_full_n_level_bids() -> NLevels<BidPrice<i32>, i32, 5> {
        let mut n_levels = NLevels::<BidPrice<i32>, i32, 5>::default();
        for i in 1..6 {
            let level = PriceLevel::new((i * 2).into());
            n_levels.try_insert_sort(level);
        }
        assert_eq!(n_levels.levels, get_price_levels([10, 8, 6, 4, 2]));
        n_levels
    }

    fn get_full_n_level_asks() -> NLevels<AskPrice<i32>, i32, 5> {
        let mut n_levels = NLevels::<AskPrice<i32>, i32, 5>::default();
        for i in 1..6 {
            let level = PriceLevel::new((i * 2).into());
            n_levels.try_insert_sort(level);
        }
        assert_eq!(n_levels.levels, get_price_levels([2, 4, 6, 8, 10]));
        n_levels
    }

    #[test]
    fn test_add_level_when_not_full() {
        let mut n_levels = NLevels::<BidPrice<i32>, i32, 2>::default();
        let level: PriceLevel<BidPrice<i32>, i32> = PriceLevel::new(1.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.worst_price, None);
        assert_eq!(n_levels.levels, [Some(PriceLevel::new(1.into())), None]);

        n_levels.try_insert_sort(PriceLevel::new(2.into()));
        assert_eq!(n_levels.worst_price, Some(1.into()));
        assert_eq!(
            n_levels.levels,
            [
                Some(PriceLevel::new(2.into())),
                Some(PriceLevel::new(1.into()))
            ]
        );
    }

    #[test]
    fn test_add_level_when_full() {
        let mut n_levels = get_full_n_level_bids();
        let level: PriceLevel<BidPrice<i32>, i32> = PriceLevel::new(12.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([12, 10, 8, 6, 4]));
        assert_eq!(n_levels.worst_price, Some(4.into()));

        let mut n_levels = get_full_n_level_bids();
        let level: PriceLevel<BidPrice<i32>, i32> = PriceLevel::new(5.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([10, 8, 6, 5, 4]));
        assert_eq!(n_levels.worst_price, Some(4.into()));

        let mut n_levels = get_full_n_level_bids();
        let level: PriceLevel<BidPrice<i32>, i32> = PriceLevel::new(3.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([10, 8, 6, 4, 3]));
        assert_eq!(n_levels.worst_price, Some(3.into()));

        let mut n_levels = get_full_n_level_asks();
        let level: PriceLevel<AskPrice<i32>, i32> = PriceLevel::new(1.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([1, 2, 4, 6, 8]));
        assert_eq!(n_levels.worst_price, Some(8.into()));

        let mut n_levels = get_full_n_level_asks();
        let level: PriceLevel<AskPrice<i32>, i32> = PriceLevel::new(3.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([2, 3, 4, 6, 8]));
        assert_eq!(n_levels.worst_price, Some(8.into()));

        let mut n_levels = get_full_n_level_asks();
        let level: PriceLevel<AskPrice<i32>, i32> = PriceLevel::new(9.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([2, 4, 6, 8, 9]));
        assert_eq!(n_levels.worst_price, Some(9.into()));
    }

    #[test]
    fn test_try_insert_level_below_worst() {
        // try_insert_sort checks if level is better than worst, so should not insert
        // insert_sort does not check if level is better than worst, so will insert
        let mut n_levels = get_full_n_level_bids();
        let level: PriceLevel<BidPrice<i32>, i32> = PriceLevel::new(1.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([10, 8, 6, 4, 2]));
        assert_eq!(n_levels.worst_price, Some(2.into()));

        n_levels.insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([10, 8, 6, 4, 1]));
        assert_eq!(n_levels.worst_price, Some(1.into()));

        let mut n_levels = get_full_n_level_asks();
        let level: PriceLevel<AskPrice<i32>, i32> = PriceLevel::new(12.into());
        n_levels.try_insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([2, 4, 6, 8, 10]));
        assert_eq!(n_levels.worst_price, Some(10.into()));

        n_levels.insert_sort(level);
        assert_eq!(n_levels.levels, get_price_levels([2, 4, 6, 8, 12]));
        assert_eq!(n_levels.worst_price, Some(12.into()));
    }

    #[test]
    fn test_replace_sort() {
        let mut n_levels = get_full_n_level_bids();
        let level: PriceLevel<BidPrice<i32>, i32> = PriceLevel::new(1.into());
        n_levels.replace_sort(6.into(), Some(level));
        assert_eq!(n_levels.levels, get_price_levels([10, 8, 4, 2, 1]));
        assert_eq!(n_levels.worst_price, Some(1.into()));

        let mut n_levels = get_full_n_level_bids();
        let level: PriceLevel<BidPrice<i32>, i32> = PriceLevel::new(1.into());
        n_levels.replace_sort(10.into(), Some(level));
        assert_eq!(n_levels.levels, get_price_levels([8, 6, 4, 2, 1]));
        assert_eq!(n_levels.worst_price, Some(1.into()));

        let mut n_levels = get_full_n_level_bids();
        let level: PriceLevel<BidPrice<i32>, i32> = PriceLevel::new(1.into());
        n_levels.replace_sort(2.into(), Some(level));
        assert_eq!(n_levels.levels, get_price_levels([10, 8, 6, 4, 1]));
        assert_eq!(n_levels.worst_price, Some(1.into()));

        let mut n_levels = get_full_n_level_asks();
        let level: PriceLevel<AskPrice<i32>, i32> = PriceLevel::new(12.into());
        n_levels.replace_sort(6.into(), Some(level));
        assert_eq!(n_levels.levels, get_price_levels([2, 4, 8, 10, 12]));
        assert_eq!(n_levels.worst_price, Some(12.into()));

        let mut n_levels = get_full_n_level_asks();
        let level: PriceLevel<AskPrice<i32>, i32> = PriceLevel::new(12.into());
        n_levels.replace_sort(10.into(), Some(level));
        assert_eq!(n_levels.levels, get_price_levels([2, 4, 6, 8, 12]));
        assert_eq!(n_levels.worst_price, Some(12.into()));

        let mut n_levels = get_full_n_level_asks();
        let level: PriceLevel<AskPrice<i32>, i32> = PriceLevel::new(12.into());
        n_levels.replace_sort(2.into(), Some(level));
        assert_eq!(n_levels.levels, get_price_levels([4, 6, 8, 10, 12]));
        assert_eq!(n_levels.worst_price, Some(12.into()));
    }
}
