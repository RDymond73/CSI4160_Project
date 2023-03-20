# ------------------------------------------------------------------------
# Original project: https://github.com/Ivan-koz/GC-IoT_Python_example
# ------------------------------------------------------------------------
import datetime
import json
import os
import ssl
import time
import jwt
import paho.mqtt.client as mqtt



# ------------------------------------------------------------------------
# CSI 4160: If using a SenseHat, then keep the following line
# No changes needed here, just showing you the changes I made
from sense_hat import SenseHat
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# CSI 4160: Replace these variables with your GCP parameters 
project_id = 'dymond-csi4160-w2023'       # Your project ID
registry_id = 'dymond-csi4160-pi'       # Your registry name.
device_id = 'dymond-csi4160-pi'  # Your device name.
# ------------------------------------------------------------------------

private_key_file = 'rsa_private.pem'  # Path to private key.
algorithm = 'RS256'  # Authentication key format.
cloud_region = 'us-central1' # Project region.
ca_certs = 'roots.pem'  # CA root certificate path.
mqtt_bridge_hostname = 'mqtt.googleapis.com'  # GC bridge hostname.
mqtt_bridge_port = 8883  # Bridge port.
message_type = 'event'  # Message type (event or state).

#additional variables for monitoring system - Rick
baseline = 32

upper_variance = 5

lower_variance = 5

status = 'running'



def create_jwt(project_id, private_key_file, algorithm):
    # Create a JWT (https://jwt.io) to establish an MQTT connection.
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    # Convert a Paho error to a human readable string.
    return '{}: {}'.format(rc, mqtt.error_string(rc))


class Device(object):
    # Device implementation.
    def __init__(self):
        self.connected = False
        # ---------------------------------------------------------------
        # CSI 4160: Only use the sense variable if you're using a SenseHat
        self.sense = SenseHat()

        # CSI 4160: Change these variables (msg and temp) to match the 
        # sensor/actuator you used in Assignment 1

        #assign local vars for PI - Rick
        self.msg = str(self.sense.get_temperature())
        self.temp = self.sense.get_temperature()
        self.baseline = baseline
        self.upper = upper_variance
        self.lower = lower_variance
        self.status = status
        #self.alert = alert
        # ---------------------------------------------------------------

    # ---------------------------------------------------------------------
    # CSI 4160: Change these two functions to match the sensor/actuator 
    # you used in Assignment 1
    def show_message(self):
        self.sense.show_message(self.msg)
   
    def get_temperature(self):
        self.temp = self.sense.get_temperature()
    # ------------------------------------------------------------------------

    def wait_for_connection(self, timeout):
        # Wait for the device to become connected.
        total_time = 0
        while not self.connected and total_time < timeout:
            time.sleep(1)
            total_time += 1

        if not self.connected:
            raise RuntimeError('Could not connect to MQTT bridge.')

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        # Callback on connection.
        print('Connection Result:', error_str(rc))
        self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        # Callback on disconnect.
        print('Disconnected:', error_str(rc))
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        # Callback on PUBACK from the MQTT bridge.
        print('Published message acked.')

    def on_subscribe(self, unused_client, unused_userdata, unused_mid,
                     granted_qos):
        # Callback on SUBACK from the MQTT bridge.
        print('Subscribed: ', granted_qos)
        if granted_qos[0] == 128:
            print('Subscription failed.')

    def on_message(self, unused_client, unused_userdata, message):
        # Callback on a subscription.
        payload = message.payload.decode('utf-8')
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(payload, message.topic, str(message.qos)))
        
        if not payload:
            return
        # Parse incoming JSON.
        data = json.loads(payload)
        # ---------------------------------------------------------------------
        # CSI 4160: Change this logic to be whatever fields you're using

        # If the data in the new message from GCP is different than what you
        # have, need to update what you have
        # if data['msg'] != self.msg:
        #     self.msg = data['msg']
        #     print('Message is: %s', self.msg)
        # have, need to update what you have

        #update status from GCP - Rick
        if data['Status'] != self.status:
            self.status = data['Status']
            print('Status: ' + self.status)
        
        #update baseline temp from GCP - Rick
        if data['Baseline Temperature'] != self.baseline:
            self.baseline = data['Baseline Temperature']
            print('Baseline Temperature is: ' + str(self.baseline))

        #update upper variance from GCP - Rick
        if data['Upper Variance'] != self.upper:
            self.upper = data['Upper Variance']
            print('Upper Variance: ' + str(self.upper))

        #update lower variance from GCP - Rick
        if data['Lower Variance'] != self.lower:
            self.lower = data['Lower Variance']
            print('Lower Variance: ' + str(self.lower))

            
        # May need to add another if statement for another piece of data
        # you're sending from GCP
        # ---------------------------------------------------------------------

def main(alert):

    client = mqtt.Client(
        client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id,
            cloud_region,
            registry_id,
            device_id))
    client.username_pw_set(
        username='unused',
        password=create_jwt(
            project_id,
            private_key_file,
            algorithm))
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    device = Device()

    client.on_connect = device.on_connect
    client.on_publish = device.on_publish
    client.on_disconnect = device.on_disconnect
    client.on_subscribe = device.on_subscribe
    client.on_message = device.on_message
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)
    client.loop_start()

    mqtt_telemetry_topic = '/devices/{}/events'.format(device_id)
    mqtt_config_topic = '/devices/{}/config'.format(device_id)

    # Wait up to 5 seconds for the device to connect.
    device.wait_for_connection(5)

    client.subscribe(mqtt_config_topic, qos=1)
    
    num_message = 0

    print("Entering try/except")
    try:        
        while True:
            # ------------------------------------------------------------------------
            # CSI 4160: Call each of the functions you defined earlier
            device.show_message()
            device.get_temperature()
            # ------------------------------------------------------------------------

            currentTime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')



            num_message += 1
            # Form payload in JSON format.
            data = {
                'Message ID' : num_message,
                # ------------------------------------------------------------------------
                # CSI 4160: Include both the sensor and actuator variables in the payload
                # you'll send to GCP
                #'msg': device.msg,
                #'Temprature': device.temp,
                # ------------------------------------------------------------------------
                'Summary': 'Temperature Report',
                'Time' : currentTime,
                'Status' : device.status,
                'Alert' : alert,
                'Temperature': device.temp, 
                'Baseline Temperature' : device.baseline,
                'Upper Variance' : device.upper,
                'Lower Variance' : device.lower
            }

            # #exit after packet is sent - Rick
            # if num_message > 1:
            #     baseline = str(data['Baseline Temperature'])
            #     upper = str(data['Upper Variance'])
            #     lower = str(data['Lower Variance'])
            #     vars3 = [baseline,upper,lower]
            #     print(vars3)
            #     return vars3 

            payload = json.dumps(data, indent=4)
            print('Publishing payload', payload)
            client.publish(mqtt_telemetry_topic, payload, qos=1)

            #exit after packet is sent - Rick
            if num_message > 1:
                baseline = data['Baseline Temperature']
                upper = data['Upper Variance']
                lower = data['Lower Variance']
                vars3 = {'base':baseline,'upper':upper,'lower':lower}
                #print(vars3)
                return baseline, upper, lower


    except KeyboardInterrupt:
        # Exit script on ^C.
        pass
        client.disconnect()
        client.loop_stop()
        # ------------------------------------------------------------------------
        # CSI 4160: Clear the SenseHat screen just to be nice
        device.sense.clear()
        # ------------------------------------------------------------------------
        print('Exit with ^C. Goodbye!')


        
# CSI 4160: Calls main function
if __name__ == '__main__':
    main('alert')

