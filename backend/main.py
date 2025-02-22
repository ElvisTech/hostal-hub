from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import db, Booking, Room, Guest
from pydantic import BaseModel
from datetime import date
from typing import Optional

# Create FastAPI instance first
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define models
class BookingBase(BaseModel):
    guest_id: int
    room_id: int
    check_in: date
    check_out: date
    status: str = 'active'

class RoomBase(BaseModel):
    number: str
    type: str
    capacity: int
    price: float
    status: str = 'available'

# Add GuestBase model after other models
class GuestBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    country: str
    document_id: str

# Add guest endpoints before the room endpoints
@app.get("/api/guests")
async def get_guests():
    with db:
        guests = list(Guest.select().dicts())
        return guests

@app.get("/api/guests/{guest_id}")
async def get_guest(guest_id: int):
    with db:
        guest = Guest.get_or_none(Guest.id == guest_id)
        if guest is None:
            raise HTTPException(status_code=404, detail="Guest not found")
        return guest.__data__

@app.post("/api/guests")
async def create_guest(guest: GuestBase):
    with db:
        new_guest = Guest.create(**guest.dict())
        return new_guest.__data__

@app.put("/api/guests/{guest_id}")
async def update_guest(guest_id: int, guest: GuestBase):
    with db:
        db_guest = Guest.get_or_none(Guest.id == guest_id)
        if db_guest is None:
            raise HTTPException(status_code=404, detail="Guest not found")
        
        for field, value in guest.dict().items():
            setattr(db_guest, field, value)
        db_guest.save()
        return db_guest.__data__

@app.delete("/api/guests/{guest_id}")
async def delete_guest(guest_id: int):
    with db:
        guest = Guest.get_or_none(Guest.id == guest_id)
        if guest is None:
            raise HTTPException(status_code=404, detail="Guest not found")
        guest.delete_instance()
        return {"message": "Guest deleted successfully"}

# Then define routes
@app.get("/api/bookings")
async def get_bookings():
    with db:
        bookings = (Booking
                   .select(Booking, Guest, Room)
                   .join(Guest, on=(Booking.guest_id == Guest.id))
                   .switch(Booking)
                   .join(Room, on=(Booking.room_id == Room.id))
                   .dicts())
        return list(bookings)

@app.get("/api/bookings/today")
async def get_today_stats():
    with db:
        today = date.today()
        checkins = Booking.select().where(Booking.check_in == today).count()
        checkouts = Booking.select().where(Booking.check_out == today).count()
        return {
            "checkins": checkins,
            "checkouts": checkouts
        }

@app.get("/api/bookings/{booking_id}")
async def get_booking(booking_id: int):
    with db:
        booking = (Booking
                  .select(Booking, Guest, Room)
                  .join(Guest)
                  .switch(Booking)
                  .join(Room)
                  .where(Booking.id == booking_id)
                  .first())
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking.__data__

@app.post("/api/bookings")
async def create_booking(booking: BookingBase):
    with db:
        # Verify guest exists
        guest = Guest.get_or_none(Guest.id == booking.guest_id)
        if guest is None:
            raise HTTPException(status_code=404, detail="Guest not found")

        # Verify room exists and is available
        room = Room.get_or_none(Room.id == booking.room_id)
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        if room.status != 'available':
            raise HTTPException(status_code=400, detail="Room is not available")

        # Create booking and update room status
        new_booking = Booking.create(**booking.dict())
        room.status = 'occupied'
        room.save()
        
        return new_booking.__data__

@app.put("/api/bookings/{booking_id}")
async def update_booking(booking_id: int, booking: BookingBase):
    with db:
        db_booking = Booking.get_or_none(Booking.id == booking_id)
        if db_booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")

        # Update booking
        for field, value in booking.dict().items():
            setattr(db_booking, field, value)
        db_booking.save()
        return db_booking.__data__

@app.delete("/api/bookings/{booking_id}")
async def delete_booking(booking_id: int):
    with db:
        booking = Booking.get_or_none(Booking.id == booking_id)
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Update room status back to available
        room = Room.get(Room.id == booking.room_id)
        room.status = 'available'
        room.save()
        
        booking.delete_instance()
        return {"message": "Booking deleted successfully"}

@app.get("/api/bookings/today")
async def get_today_stats():
    with db:
        today = date.today()
        checkins = Booking.select().where(Booking.check_in == today).count()
        checkouts = Booking.select().where(Booking.check_out == today).count()
        return {
            "checkins": checkins,
            "checkouts": checkouts
        }

@app.get("/api/rooms")
async def get_rooms():
    with db:
        rooms = list(Room.select().dicts())
        return rooms

# Add stats endpoint before the room_id endpoint
@app.get("/api/rooms/stats")
async def get_room_stats():
    with db:
        total_rooms = Room.select().count()
        available_rooms = Room.select().where(Room.status == 'available').count()
        occupied_rooms = Room.select().where(Room.status == 'occupied').count()
        maintenance_rooms = Room.select().where(Room.status == 'maintenance').count()
        return {
            "total": total_rooms,
            "available": available_rooms,
            "occupied": occupied_rooms,
            "maintenance": maintenance_rooms
        }

@app.get("/api/rooms/available")
async def get_available_rooms():
    with db:
        rooms = list(Room.select().where(Room.status == 'available').dicts())
        return rooms

@app.get("/api/rooms/{room_id}")
async def get_room(room_id: int):
    with db:
        room = Room.get_or_none(Room.id == room_id)
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        return room.__data__

@app.post("/api/rooms")
async def create_room(room: RoomBase):
    with db:
        new_room = Room.create(**room.dict())
        return new_room.__data__

@app.put("/api/rooms/{room_id}")
async def update_room(room_id: int, room: RoomBase):
    with db:
        db_room = Room.get_or_none(Room.id == room_id)
        if db_room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        
        for field, value in room.dict().items():
            setattr(db_room, field, value)
        db_room.save()
        return db_room.__data__

@app.delete("/api/rooms/{room_id}")
async def delete_room(room_id: int):
    with db:
        room = Room.get_or_none(Room.id == room_id)
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        room.delete_instance()
        return {"message": "Room deleted successfully"}

# Add this endpoint with the other room endpoints
@app.get("/api/rooms/stats")
async def get_room_stats():
    with db:
        total_rooms = Room.select().count()
        available_rooms = Room.select().where(Room.status == 'available').count()
        occupied_rooms = Room.select().where(Room.status == 'occupied').count()
        maintenance_rooms = Room.select().where(Room.status == 'maintenance').count()
        return {
            "total": total_rooms,
            "available": available_rooms,
            "occupied": occupied_rooms,
            "maintenance": maintenance_rooms
        }