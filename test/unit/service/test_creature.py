import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from models.creature import Creature
from service import creature as code

sample = Creature(
    name = "Yeti", 
    country="CN",
    area="Himalayas", 
    description="Hirsute Himalayan",
    aka = "Abominable Snowman",
)

def test_create():
    resp = code.create(sample)
    assert resp == sample

def test_get_exists():
    resp = code.get_one("Yeti")
    assert resp == sample

def test_get_not_exists():
    resp = code.get_one("not_exists")
    assert resp is None