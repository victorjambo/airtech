import os
import jwt
import json

from locust import HttpLocust, TaskSet, task
from locust.main import runners
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from api.models import User, Flight, Ticket
from api.utilities.constants import CHARSET
from api.utilities.constants import MIMETYPE

BASE_URL = "/api/v1"
fake = Faker()


class UserBehaviour(TaskSet):
  def on_start(self):
    # user signup
    user_data = {
      "username": fake.name(),
      "email": fake.email(),
      "password": "password1234"
    }
    signup_response = self.client.post(f'{BASE_URL}/auth/signup', data=json.dumps(user_data), headers={
      'Content-Type': MIMETYPE,
      'Accept': MIMETYPE
    },
    name="Signup")
    signup_response_json = json.loads(signup_response.content.decode(CHARSET))
    self.current_user = {
      "username": signup_response_json["data"]["username"],
      "email": signup_response_json["data"]["email"],
      "id": signup_response_json["data"]["id"]
    }

    self.headers = {
      'Content-Type': MIMETYPE,
      'Accept': MIMETYPE,
      'Authorization': f'Bearer {jwt.encode({"data": self.current_user}, "4BZGxmctLXuqDEyMqEbaqdCkM").decode(CHARSET)}'
    }

    # flight id
    flight_response = self.client.get(f'{BASE_URL}/flights', headers=self.headers, name="List Flights")
    flight_response_json = json.loads(flight_response.content.decode(CHARSET))
    if len(flight_response_json["data"]) == 0:
      print(">>>>>", "Create a flight", "<<<<<")
      runners.locust_runner.quit()

    self.flight_id = flight_response_json["data"][0]["id"]

    # ticket id
    ticket_response = self.client.get(
      f'{BASE_URL}/flights/{self.flight_id}/tickets',
      headers=self.headers,
      name="List Tickets")
    ticket_response_json = json.loads(ticket_response.content.decode(CHARSET))
    if len(ticket_response_json["data"]) == 0:
      print(">>>>>", "Create a ticket", "<<<<<")
      runners.locust_runner.quit()

    self.ticket_id = ticket_response_json["data"][0]["id"]

  @task(1)
  def home(self):
    self.client.get("/",
      headers=self.headers,
      name="Home")

  @task(2)
  def login(self):
    self.client.post(f'{BASE_URL}/auth/login', data=json.dumps({
        "username": "victor",
        "password": "password1234"
      }),
      headers=self.headers,
      name="Login")

  @task(2)
  def get_flights(self):
    self.client.get(f'{BASE_URL}/flights',
      headers=self.headers,
      name="Get Flights")

  @task(2)
  def get_single_flight(self):
    self.client.get(f'{BASE_URL}/flights/{self.flight_id}',
      headers=self.headers,
      name="Get Single Flight")

  @task(2)
  def book_ticket(self):
    self.client.post(f'{BASE_URL}/flights/{self.flight_id}/tickets',
      data=json.dumps({
        "seatNumber": fake.pystr(),
        "destination": fake.city(),
        "travelDate": "2090-10-10"
      }),
      headers=self.headers,
      name="Book Ticket")

  @task(2)
  def get_ticket(self):
    self.client.get(f'{BASE_URL}/flights/{self.flight_id}/tickets',
      headers=self.headers,
      name="Get All Tickets")

  @task(2)
  def get_ticket(self):
    self.client.get(f'{BASE_URL}/tickets/{self.ticket_id}',
      headers=self.headers,
      name="Get Single Ticket")


class WebsiteUser(HttpLocust):
  task_set = UserBehaviour
  min_wait = 5000
  max_wait = 15000
