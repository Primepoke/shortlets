from datetime import date, timedelta

def is_property_available(property, start_date, end_date):
    if property.is_available:
        return True
    else:
        bookings = property.bookings.filter(is_confirmed=True)

        for booking in bookings:
            booked_start_date = booking.check_in_date
            booked_end_date = booking.check_out_date

            # Check for date range overlap
            if not (end_date < booked_start_date or start_date > booked_end_date):
                return False  # Overlapping date range, property is not available

        return True  # No overlapping date range found, property is available

