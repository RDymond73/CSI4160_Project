# CSI4160_Project
Temperature Monitoring Raspberry PI

FILES NEEDED IN WORKING DIRECTORY
  1. roots.pem
  2. rsa_private.pem
  3. rsa_public.pem
  
Make changes to sensehat.py to connect to your gcp IoT:
  - config needs to be set from gcp in the following format
  
  {
"Status":"running",
"Baseline Temperature":"95",
"Upper Variance":"10",
"Lower Variance":"10"
}

- baseline, upper variance, and lower variance can be changed 
- do not change status

monitor.py is the main script to run


