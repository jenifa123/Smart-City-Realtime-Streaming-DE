import  os
import time
import uuid

from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime, timedelta
import random

LONDON_COORDINATES = {
    "latitude": 51.5074,
    "longitude": -0.1278,
}

BIRMINGHAM_COORDINATES = {
    "latitude": 52.4862,
    "longitude": -1.8904,
}

#calculate the movement increments
LATITUDE_INCREMENT= (BIRMINGHAM_COORDINATES['latitude']-  LONDON_COORDINATES['latitude'])/100
LONGITUDE_INCREMENT= (BIRMINGHAM_COORDINATES['longitude']-  LONDON_COORDINATES['longitude'])/100

#Env variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS','localhost:9092')
#vehicle information
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC','vehicle_data')
#gps information
GPS_TOPIC = os.getenv('GPS_TOPIC','gps_data')
#traffic information
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC','traffic_data')
#weather information
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC','weather_data')
#emergency information
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC','emergency_data')

random.seed(42)
#start location and the time we start
start_time = datetime.now()
start_location = LONDON_COORDINATES.copy()


def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30,60))
    return start_time

def delivery_report(err,msg):
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} topic and [{}] partition ".format(msg.topic(), msg.partition()))

def json_serializer(obj):
    if isinstance(obj,uuid.UUID):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def produce_data_to_kafka(producer, topic,data):
    producer.produce(
        topic,
        key=str(data['id']),
        value=json.dumps(data,default=json_serializer).encode('utf-8'),
        on_delivery=delivery_report
    )
    producer.flush()

def generate_gps_data(device_id, timestamp,vehicle_type='Private'):
    return {
        'id':uuid.uuid4(),
        'deviceId':device_id,
        'timestamp':timestamp,
        'speed':random.uniform(0,40),
        'direction':'North-East',
        'vehicleType':vehicle_type,
    }

def simulate_vehicle_movement():
    global start_location
    #move towards birmingham
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT

    #adding some random value to simulate actual road travel
    start_location['latitude'] += random.uniform(-0.0005,0.0005)
    start_location['longitude'] += random.uniform(-0.0005,0.0005)
    return start_location

def generate_weather_data(device_id, timestamp,location):
    return {
        'id':uuid.uuid4(),
        'deviceId':device_id,
        'location':location,
        'timestamp':timestamp,
        'temperature':random.uniform(-5,26),
        'weatherCondition': random.choice(['Sunny','Cloudy','Rainy','Snow']),
        'precipitation': random.uniform(0,25),
        'windSpeed': random.uniform(0,100),
        'humidity': random.uniform(0,100),
        'airQualityIndex': random.uniform(0,500),

    }

def generate_emergency_incident_data(device_id, timestamp,location):
    return {
        'id':uuid.uuid4(),
        'deviceId':device_id,
        'incidentId':uuid.uuid4(),
        'type':random.choice(['Fire','Accident','Medical','Police','None']),
        'timestamp':timestamp,
        'location':location,
        'status': random.choice(['Active','Resolved']),
        'description':'Incident Description'
    }

def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitude'], location['longitude']),
        'speed': random.uniform(10,40),
        'direction': 'North-East',
        'make':'BMW',
        'model':'C500',
        'year':2025,
        'fuelType':'Hybrid'
    }

def generate_traffic_camera_date(device_id,timestamp,location,camera_id):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'cameraId': camera_id,
        'location': location,
        'timestamp': timestamp,
        'snapshot':'Base64EncodedString'
    }

def simulate_journey(producer, device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id,vehicle_data['timestamp'])
        traffic_camera_data = generate_traffic_camera_date(device_id,vehicle_data['timestamp'],vehicle_data['location'],'Nikon-Cam123')
        weather_data = generate_weather_data(device_id,vehicle_data['timestamp'],vehicle_data['location'])
        emergency_incident_data = generate_emergency_incident_data(device_id,vehicle_data['timestamp'],vehicle_data['location'])
        #vehicle reached target
        if (vehicle_data['location'][0] >= BIRMINGHAM_COORDINATES['latitude']
        and vehicle_data['location'][1] <= BIRMINGHAM_COORDINATES['longitude']):
            print("Vehicle has reached Birmingham. Ending Simulation")
            break

        produce_data_to_kafka(producer,VEHICLE_TOPIC,vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC, traffic_camera_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emergency_incident_data)

        '''
        print(f"Vehicle Data : {vehicle_data}")
        print(f"GPS Data : {gps_data}")
        print(f"Traffic Camera Data : {traffic_camera_data}")
        print(f"Weather Data : {weather_data}")
        print(f"Emergency Incident Data : {emergency_incident_data}")
        '''
        time.sleep(5)

if __name__ == '__main__':
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print('Kafka Error: {}'.format(err)),
    }
    producer = SerializingProducer(producer_config)

    try:
        simulate_journey(producer,'Vehicle-JN')

    except KeyboardInterrupt:
        print("Simulation stopped by user")
    except Exception as err:
        print("Unexpected error occurred:", err)
