from flask_table import Table, ButtonCol, Col, DateCol


class DVD_table(Table):
    id = Col('Id', show=False)
    title = Col('Title')
    owner_id = Col('Owner Id', show=False)
    owner_name = Col('Owner')
    format_dvd = Col('DVD')
    format_bluray = Col('Blu Ray')
    format_4k = Col('4K')
    rating = Col('Rating')
    borrower_name = Col('Borrower')
    date_borrowed = DateCol('Borrowed', date_format='long')
    borrow_dvd = ButtonCol('Borrow', 'borrow_dvd', url_kwargs=dict(id='id'))
    return_dvd = ButtonCol('Return', 'return_dvd', url_kwargs=dict(id='id'))

class Mag_table(Table):
    id = Col('Id', show=False)
    title = Col('Title')
    owner_id = Col('Owner Id', show=False)
    owner_name = Col('Owner')
    borrower_name = Col('Borrower')
    date_borrowed = DateCol('Borrowed', date_format='long')
    borrow_mag = ButtonCol('Borrow', 'borrow_mag', url_kwargs=dict(id='id'))
    return_mag = ButtonCol('Return', 'return_mag', url_kwargs=dict(id='id'))