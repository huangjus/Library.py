# Author: Justin Huang
# GitHub username: huangjus
# Date: 4/18/23
# Description: Implements a library simulator using multiple classes, including LibraryItem, Patron, and Library,
# as well as three subclasses of LibraryItem called Book, Album, and Movie. The code allows for the creation of
# library items and patrons, and the simulation of checkouts, returns, requests, and fines. The Library class manages
# the holdings and members, and also tracks the current date for fine calculations.

class LibraryItem:
    """
    A LibraryItem object represents a library item that a patron can check out from a library.
    """
    def __init__(self, library_item_id, title):
        self._library_item_id = library_item_id
        self._title = title
        self._location = "ON_SHELF"
        self._checked_out_by = None
        self._requested_by = None
        self._date_checked_out = None

    def get_library_item_id(self):
        """Returns the library item ID."""
        return self._library_item_id

    def get_title(self):
        """Returns the title of the library item."""
        return self._title

    def get_location(self):
        """Returns the location of the library item."""
        return self._location

    def set_location(self, location):
        """Sets the location of the library item."""
        self._location = location

    def get_checked_out_by(self):
        """Returns the patron who has the library item checked out."""
        return self._checked_out_by

    def set_checked_out_by(self, patron):
        """Sets the patron who has the library item checked out."""
        self._checked_out_by = patron

    def get_requested_by(self):
        """Returns the patron who has requested the library item."""
        return self._requested_by

    def set_requested_by(self, patron):
        """Sets the patron who has requested the library item."""
        self._requested_by = patron

    def get_date_checked_out(self):
        """Returns the date the library item was checked out."""
        return self._date_checked_out

    def set_date_checked_out(self, date):
        """Sets the date the library item was checked out."""
        self._date_checked_out = date


class Book(LibraryItem):
    """
    A Book object represents a book in a library that inherits from LibraryItem.
    """
    def __init__(self, library_item_id, title, author):
        super().__init__(library_item_id, title)
        self._author = author

    def get_author(self):
        """Returns the author of the book."""
        return self._author

    def get_check_out_length(self):
        """Returns the number of days the book may be checked out for."""
        return 21


class Album(LibraryItem):
    """
    An Album object represents an album in a library that inherits from LibraryItem.
    """
    def __init__(self, library_item_id, title, artist):
        super().__init__(library_item_id, title)
        self._artist = artist

    def get_artist(self):
        """Returns the artist of the album."""
        return self._artist

    def get_check_out_length(self):
        """Returns the number of days the album may be checked out for."""
        return 14


class Movie(LibraryItem):
    """
    A Movie object represents a movie in a library that inherits from LibraryItem.
    """
    def __init__(self, library_item_id, title, director):
        super().__init__(library_item_id, title)
        self._director = director

    def get_director(self):
        """Returns the director of the movie."""
        return self._director

    def get_check_out_length(self):
        """Returns the number of days the movie may be checked out for."""
        return 7


class Patron:
    """
    A Patron object represents a patron of a library.
    """
    def __init__(self, patron_id, name):
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = []
        self._fine_amount = 0

    def get_patron_id(self):
        """Returns the patron ID."""
        return self._patron_id

    def get_name(self):
        """Returns the patron's name."""
        return self._name

    def get_checked_out_items(self):
        """Returns the collection of LibraryItems that the Patron has checked out."""
        return self._checked_out_items

    def get_fine_amount(self):
        """Returns the fine amount the Patron owes the Library."""
        return self._fine_amount

    def set_fine_amount(self, fine_amount):
        """Sets the fine amount the Patron owes the Library."""
        self._fine_amount = fine_amount

    def add_library_item(self, library_item):
        """
        Adds the specified LibraryItem to the collection of checked_out_items.
        """
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        """
        Removes the specified LibraryItem from the collection of checked_out_items.
        """
        self._checked_out_items.remove(library_item)

    def amend_fine(self, amount):
        """
        Amends the fine amount the Patron owes the Library. A positive argument increases the fine_amount, a negative
        one decreases it.
        """
        self._fine_amount += amount


class Library:
    """
    A Library object represents a library that contains various library items and is used by various patrons.
    """

    def __init__(self):
        self._holdings = []
        self._members = []
        self._current_date = 0

    def add_library_item(self, library_item):
        """
        Adds a LibraryItem object to the library's holdings.
        """
        self._holdings.append(library_item)

    def add_patron(self, patron):
        """
        Adds a Patron object to the library's members.
        """
        self._members.append(patron)

    def lookup_library_item_from_id(self, library_item_id):
        """
        Returns the LibraryItem object corresponding to the given library_item_id, or None if not found in holdings.
        """
        for item in self._holdings:
            if item.get_library_item_id() == library_item_id:
                return item
        return None

    def lookup_patron_from_id(self, patron_id):
        """
        Returns the Patron object corresponding to the given patron_id, or None if not found in members.
        """
        for patron in self._members:
            if patron.get_patron_id() == patron_id:
                return patron
        return None

    def check_out_library_item(self, patron_id, library_item_id):
        """
        Checks out a LibraryItem to a Patron if possible, and returns the result as a string message.
        """
        patron = self.lookup_patron_from_id(patron_id)
        if not patron:
            return "patron not found"

        library_item = self.lookup_library_item_from_id(library_item_id)
        if not library_item:
            return "item not found"

        if library_item.get_checked_out_by():
            return "item already checked out"

        if library_item.get_requested_by() and library_item.get_requested_by() != patron:
            return "item on hold by other patron"

        library_item.set_checked_out_by(patron)
        library_item.set_date_checked_out(self._current_date)
        library_item.set_location("CHECKED_OUT")

        if library_item.get_requested_by() == patron:
            library_item.set_requested_by(None)

        patron.add_library_item(library_item)

        return "check out successful"

    def return_library_item(self, library_item_id):
        """
        Returns a LibraryItem to the library if possible, and returns the result as a string message.
        """
        library_item = self.lookup_library_item_from_id(library_item_id)
        if not library_item:
            return "item not found"

        if not library_item.get_checked_out_by():
            return "item already in library"

        patron = library_item.get_checked_out_by()
        patron.remove_library_item(library_item)

        if library_item.get_requested_by():
            library_item.set_location("ON_HOLD_SHELF")
        else:
            library_item.set_location("ON_SHELF")

        library_item.set_checked_out_by(None)

        return "return successful"

    def request_library_item(self, patron_id, library_item_id):
        """
        Processes a request for a library item by a patron. Returns a string message with the result.
        """
        patron = self.lookup_patron_from_id(patron_id)
        if not patron:
            return "patron not found"

        library_item = self.lookup_library_item_from_id(library_item_id)
        if not library_item:
            return "item not found"

        if library_item.get_requested_by() is not None:
            return "item already on hold"

        library_item.set_requested_by(patron)
        if library_item.get_location() == "ON_SHELF":
            library_item.set_location("ON_HOLD_SHELF")

        return "request successful"

    def pay_fine(self, patron_id, amount):
        """
        Processes a fine payment for the given patron_id and amount. Returns a string message with the result.
        """
        patron = self.lookup_patron_from_id(patron_id)
        if not patron:
            return "patron not found"

        patron.amend_fine(-amount)
        return "payment successful"

    def increment_current_date(self):
        """
        Increments the current date and updates fines for overdue LibraryItems.
        """
        self._current_date += 1
        for patron in self._members:
            for library_item in patron.get_checked_out_items():
                due_date = library_item.get_date_checked_out() + library_item.get_check_out_length()
                if self._current_date > due_date:
                    patron.amend_fine(0.10)
