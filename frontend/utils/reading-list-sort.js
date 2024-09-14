/**
 * Provides a function usable with `array.filter` to dedup books.
 *
 * @returns {function(*, *, *): boolean}
 */
function bookDeduper(){
  let bookIds = null;
  return (entry, index, entries) => {
    if(!bookIds){
      bookIds = entries.map(b => b.book.id);
    }
    return bookIds.indexOf(entry.book.id) === index;
  }
}

/**
 * Retrieve the first entry of each list ordered by publication date.
 *
 * @param readingLists
 * @returns {*}
 */
function getNextReadingListEntries(readingLists) {
  return readingLists
    // Take the next entry of each reading list
    .map(list => {
      return list.entries.length > 0 ? list.entries[0] : null;
    })
    // Remove empty reading list entries
    .filter(a => a)
    // Remove duplicates
    .filter(bookDeduper())
    // Sort books by pub date
    .sort((a, b) => {
      a.book.pub_time = a.book.pub_time || new Date(a.book.pub_date).getTime();
      b.book.pub_time = b.book.pub_time || new Date(b.book.pub_date).getTime();
      return a.book.pub_time >= b.book.pub_time ? 1 : -1;
    });
}

/**
 * Look for dependencies between books and provide a list of dependencies.
 * This is used to try to fix issues if two lists are in conflict.
 *
 * @param nextBooks
 * @param readingLists
 * @returns {*[]}
 */
function findBooksDependencies(nextBooks, readingLists) {
  const dependencies = [];

  nextBooks.forEach((book) => {
    // Look for entries in other reading lists that are not the first entry
    const blockingLists = readingLists.filter(r => r.entries.map(e => e.book.id).indexOf(book.book.id) > 0);
    if (blockingLists.length > 0) {
      // Save the reading list and the first entry in the list (the one blocking)
      dependencies.push([book, blockingLists.map(l => [l, l.entries[0]])]);
    }
  });
  return dependencies;
}

/**
 * Check if a book is in first place of every list it is in.
 *
 * @param entry
 * @param readingLists
 * @returns {boolean}
 */
function isFirstInEveryList(entry, readingLists){
  return !readingLists.find(
      r => r.entries.map(e => e.book.id).indexOf(entry.book.id) > 0
    )
}

/**
 * List every books that could be the next in the list.
 *
 * @param nextBooks
 * @param readingLists
 * @returns {*}
 */
function findPossibleBooks(nextBooks, readingLists) {
  let lowestDate = null;
  const [possibleBooks] = nextBooks.reduce(([books, shouldContinue], entry) => {
    if (!shouldContinue || lowestDate < entry.book.pub_time) {
      return [books, false];
    }
    // Check if book is not in another reading list
    // If it's the first entry of a list, we don't care about it. (as it is also a candidate for next book)
    const candidate = isFirstInEveryList(entry, readingLists);
    if (candidate) {
      lowestDate = Math.min(lowestDate, entry.book.pub_time);
      books.push(entry);
      return [books, true];
    }
    return [books, true];
  }, [[], true]);
  return possibleBooks;
}

/**
 * Select the next book among the potential candidates.
 *
 * @param nextBooks
 * @param readingLists
 * @param wantBlockedBooks
 * @returns {(*|*[])[]|*[]}
 */
function findNextBook(nextBooks, readingLists, wantBlockedBooks = true) {
  const nextBook = findPossibleBooks(nextBooks, readingLists)[0];
  if (nextBook) {
    return [nextBook, null];
  }

  // This is an edge case if there is two lists with circular dependency
  return [
    // If no book was the first of every list, we just take the older one first
    nextBooks[0],
    // This block of code tries to give enough information to identify the cause of the circular dependency
    wantBlockedBooks ? findBooksDependencies(nextBooks, readingLists) : null
  ];
}

/**
 * Sort reading lists to provide a list of books to read in order.
 *
 * @param {object[]} readingLists Reading Lists to sort for what's next
 * @returns {[object[],object[]|null]}
 */
export function sortReadingLists(readingLists) {
  const originalReadingLists = JSON.parse(JSON.stringify(readingLists));
  const booksToRead = [];
  let blockedBooks = null;

  while (true) {
    // Fetch the next book in each list sorted by date
    const nextBooks = getNextReadingListEntries(readingLists);
    // No books left
    if (nextBooks.length === 0) {
      break;
    }

    const [nextBook, newBlockedBooks] = findNextBook(nextBooks, readingLists, !!blockedBooks);
    blockedBooks = blockedBooks || newBlockedBooks;

    nextBook.lists = [];

    // Clean the selected books from all reading lists
    readingLists.forEach(r => {
      const entries = r.entries.map(e => e.book.id);
      const index = entries.indexOf(nextBook.book.id);
      if (index >= 0) {
        r.entries.splice(index, 1);
        nextBook.lists.push(originalReadingLists.find(or => or.id === r.id));
      }
    });

    booksToRead.push(nextBook);

    // Find empty reading lists and create an entry for "empty reading list"
    const emptyReadingLists = readingLists.filter(list => list.entries.length === 0);
    emptyReadingLists.forEach(list => {
      readingLists.splice(readingLists.indexOf(list), 1);

      booksToRead.push({
        id: "list" + list.id,
        type: "empty_list",
        list
      });
    });
  }

  return [booksToRead, blockedBooks];
}
