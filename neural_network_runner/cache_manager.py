from neural_network_runner import _set_cache
from models import NeuralNetwork
from db import db


def set_network_cache():
    _set_cache(NeuralNetwork.query.first().code)


def update_network_code(new_code):
    main_record = NeuralNetwork.query.first()
    main_record.code = new_code
    db.session.commit()
    set_network_cache()
