import requests
import os
from sqlalchemy import func
from db import db
from models import Donation, Team, Building
from neural_network_runner.cache_manager import update_network_code
from utils.network_input import encodeInput, STANDARDIZE_TYPE_EARNINGS

TRAINER_INTEGRATION_TOKEN = os.environ.get("TRAINER_INTEGRATION_TOKEN", "local")
TRAINER_HOST = os.environ.get("TRAINER_HOST", "http://localhost:5001")


def train_model(campaign_id):
    total_donations_per_building = db.session.query(Building.id, func.sum(Donation.amount)).join(Team).join(
        Building).filter(Team.campaign_id == campaign_id).group_by(Building.id).all()
    buildings_for_donations = Building.query.filter(
        Building.id.in_([d[0] for d in total_donations_per_building])).all()
    building_by_id = {b.id: b for b in buildings_for_donations}

    new_model_data = []

    for building_id, total_donation in total_donations_per_building:
        building = building_by_id[building_id]
        neural_network_input = building.get_encoded_input()
        neural_network_input['currentYearEarnings'] = encodeInput(total_donation, STANDARDIZE_TYPE_EARNINGS)

        new_model_data.append(neural_network_input)

    url = "{trainer_host}/train".format(trainer_host=TRAINER_HOST)

    response = requests.post(url, json=new_model_data,
                             headers={'Authorization': "Bearer {}".format(TRAINER_INTEGRATION_TOKEN)})
    response.raise_for_status()

    update_network_code(response.text)
