#!/bin/bash

# Install ChromeDriver
if command -v chromedriver &> /dev/null; then
    echo "ChromeDriver is already installed."
else
    echo "Installing ChromeDriver..."
    brew install --cask chromedriver
fi

# Check ChromeDriver installed
CHROMEDRIVER_PATH=$(which chromedriver)
if [ -z "$CHROMEDRIVER_PATH" ]; then
	echo -e "\033[31mError: ChromeDriver installation failed.\033[0m"  exit 1
fi

# Create symbolic link for ChromeDriver
if [ ! -L "./chromedriver" ]; then
  echo "Creating symbolic link for ChromeDriver..."
  ln -s "$CHROMEDRIVER_PATH" ./chromedriver
fi

# “Adjusting ChromeDriver Security Settings in present working dir”
echo "Removing quarantine attribute from ChromeDriver..."
xattr -d com.apple.quarantine ./chromedriver || echo "Quarantine attribute not found."

# Create Python virtual env
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

# Generate requirements.txt dynamically
REQUIREMENTS_FILE="requirements.txt"
echo "selenium" > $REQUIREMENTS_FILE
echo "python-dotenv" >> $REQUIREMENTS_FILE

# Activate virtual environment and install packages
source venv/bin/activate

# Generate requirements.txt dynamically
REQUIREMENTS_FILE="requirements.txt"
echo "selenium" > $REQUIREMENTS_FILE
echo "python-dotenv" >> $REQUIREMENTS_FILE

echo "Installing required Python packages..."
pip install --upgrade pip
pip install -r $REQUIREMENTS_FILE
# Remove the requirements.txt after installation
rm $REQUIREMENTS_FILE

deactivate

# Set up cron job
CRON_JOB="0 8 * * * $(pwd)/venv/bin/python3 $(pwd)/get_cabi_coin.py"
CRON_FILE="cronjob_tmp"

# Update cron jobs
echo "Updating cron jobs..."
crontab -l | grep -v "$(pwd)/get_cabi_coin.py" > $CRON_FILE
echo "$CRON_JOB" >> $CRON_FILE
crontab $CRON_FILE
rm $CRON_FILE

echo "Setup complete! Your script will run every day at 8:00 AM."