from datetime import datetime, timedelta

next_24 = str(datetime.utcnow() + timedelta(hours=24)).split(".")[0]

ticket_data = [
  {
    "seat_number": "KQ123",
    "destination": "New York",
    "travel_date": next_24
  },
  {
    "seat_number": "KQ124",
    "destination": "New York",
    "travel_date": next_24
  },
  {
    "seat_number": "KQ125",
    "destination": "New York",
    "travel_date": next_24
  },
  {
    "seat_number": "KQ126",
    "destination": "New York",
    "travel_date": next_24
  },
  {
    "seat_number": "KQ127",
    "destination": "New York",
    "travel_date": next_24
  },
  {
    "seat_number": "KQ128",
    "destination": "New York",
    "travel_date": next_24
  }
]