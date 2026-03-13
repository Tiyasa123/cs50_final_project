import pytest 
import project

def test_feedback():
  assert project.feedback(20) == "Good start!"
  assert project.feedback(100) == "You're in the zone!"
  assert project.feedback(200) == "Impressive!"
  assert project.feedback(340) == "Incredible dedication"
  assert project.feedback(400) == "Don't overdo it"
  assert project.feedback(650) == "Don't drain yourself"

def test_convert():
  assert project.convert("9:30 AM to 5:00 PM") == "09:30 to 17:00"
  assert project.convert("9 AM to 5 PM") == "09:00 to 17:00"
  assert project.convert("10 AM to 8:50 PM") == "10:00 to 20:50"

def test_welcome():
  assert project.welcome("Roy") == "🌈 Hello Roy! Let's turn ideas into action it's time to conquer the day!"
