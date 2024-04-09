function getNextReadingListEntries(readingLists) {
  return readingLists
    // Take the next entry of each reading list
    .map(list => {
      return list.entries.length > 0 ? list.entries[0] : null;
    })
    // Remove empty reading list entries
    .filter(a => a)
    // Sort books by pub date
    .sort((a, b) => {
      a.book.pub_time = a.book.pub_time || new Date(a.book.pub_date).getTime();
      b.book.pub_time = b.book.pub_time || new Date(b.book.pub_date).getTime();
      return a.book.pub_time >= b.book.pub_time ? 1 : -1;
    });
}

function findBooksDependencies(nextBooks, readingLists) {
  const bookIds = nextBooks.map(b => b.book.id);
  // Remove duplicates
  const booksToConsider = nextBooks.filter((book, index) => bookIds.indexOf(book.book.id) === index);

  const dependencies = [];

  booksToConsider.forEach((book) => {
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

    let nextBook = nextBooks.find(entry => {
      // Check if book is not in another reading list
      // If it's the first entry of a list, we don't care about it. (as it is also a candidate for next book)
      return !readingLists.find(
        r => r.entries.map(e => e.book.id).indexOf(entry.book.id) > 0
      );
    });

    // This is an edge case if there is two lists with circular dependency
    if (!nextBook) {
      // This block of code tries to give enough information to identify the cause of the circular dependency
      if (!blockedBooks) {
        blockedBooks = findBooksDependencies(nextBooks, readingLists);
      }
      // If no book was the first of every list, we just take the older one first
      nextBook = nextBooks[0];
    }

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
    const emptyReadingLists = readingLists.filter(list => {
      return list.entries.length === 0;
    });
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
