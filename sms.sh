echo "Going into project folder..."
cd '/home/vagrant/src/trails project'

echo "setting up environment"
source env/bin/activate

echo "cooking secrets..."
source secret.sh

echo "Doing the magic 🤓..."
python3 send_sms.py

