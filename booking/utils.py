from datetime import date, timedelta

def is_property_available(property, start_date, end_date):
    if start_date < date.today() or end_date < date.today():
        return None, "One or more of the date you entered is past. Enter correct dates and check again."
    
    if property.is_available:
        bookings = property.bookings.filter(confirmation_status='confirmed')

        for booking in bookings:
            booked_start_date = booking.check_in_datetime.date()
            booked_end_date = booking.check_out_datetime.date()

            # Check for date range overlap
            if not (end_date < booked_start_date or start_date > booked_end_date):
                # Overlapping date range, property is not available
                return False, f"This property is not available from {start_date.isoformat()} to {end_date.isoformat()}."  

        # No overlapping date range, property is available
        return True, f"This property is Available for Booking from {start_date.isoformat()} to {end_date.isoformat()}. BOOK NOW!"

