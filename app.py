from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ascend.db"
db = SQLAlchemy(app)


class DeviceModel(db.Model):
    """"""

    # Page 1
    id = db.Column(db.Integer, primary_key=True)
    owner_ref = db.Column(db.String(), nullable=False)
    serial_number = db.Column(db.String(), nullable=False)
    device_type = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    img_url = db.Column(db.String(), nullable=False)

    # Page 2
    temp = db.Column(db.Float, nullable=False)
    operating_hours = db.Column(db.Integer, nullable=False)
    analogue_in = db.Column(db.Float, nullable=False)
    spool_position = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)
    flow_torque = db.Column(db.Integer, nullable=False)

    # Page 3
    signal_type = db.Column(db.String(), nullable=False)
    signal_range_low = db.Column(db.Float, nullable=False)
    signal_range_high = db.Column(db.Float, nullable=False)
    flow_limit = db.Column(db.Integer, nullable=False)
    pressure_controller = db.Column(db.String(), nullable=False)

    # Page 4
    uptime = db.Column(db.Integer, nullable=False)
    cycles = db.Column(db.Integer, nullable=False)
    issues = db.Column(db.Integer, nullable=False)

    def __repr__(self):

        return f"Device(name = {owner_ref}, device_type = {device_type}, location = {location}, status = {status})"


device_update_args = reqparse.RequestParser()
device_update_args.add_argument(
    "signal_type",
    type=str,
    help="signal_type",
)
device_update_args.add_argument(
    "signal_range_low",
    type=float,
    help="signal_range_low",
)
device_update_args.add_argument(
    "signal_range_high",
    type=float,
    help="signal_range_high",
)
device_update_args.add_argument(
    "flow_limit",
    type=int,
    help="signal_range_high",
)
device_update_args.add_argument(
    "pressure_controller",
    type=str,
    help="pressure_controller",
)

resource_fields = {
    "id": fields.Integer,
    "owner_ref": fields.String,
    "serial_number": fields.String,
    "device_type": fields.String,
    "location": fields.String,
    "status": fields.String,
    "img_url": fields.String,
}

full_resource_fields = {
    "id": fields.Integer,
    "owner_ref": fields.String,
    "serial_number": fields.String,
    "device_type": fields.String,
    "location": fields.String,
    "status": fields.String,
    "img_url": fields.String,
    "temp": fields.Float,
    "operating_hours": fields.Integer,
    "analogue_in": fields.Float,
    "spool_position": fields.Float,
    "pressure": fields.Float,
    "flow_torque": fields.Integer,
    "signal_type": fields.String,
    "signal_range_low": fields.Float,
    "signal_range_high": fields.Float,
    "flow_limit": fields.Integer,
    "pressure_controller": fields.String,
    "uptime": fields.Integer,
    "cycles": fields.Integer,
    "issues": fields.Integer,
}

control_resource_fields = {
    "id": fields.Integer,
    "flow_torque": fields.Integer,
    "signal_type": fields.String,
    "signal_range_low": fields.Float,
    "signal_range_high": fields.Float,
    "flow_limit": fields.Integer,
    "pressure_controller": fields.String,
}


class Device(Resource):
    """Supports GET and PUT requests.
    GET reads data from SQL database.
        returns basic information database entries for mathing owner_ref
        see "full_resource_fields" for attributes
    """

    @marshal_with(resource_fields)
    def get(self, user_id):
        result = DeviceModel.query.filter_by(owner_ref=user_id).all()
        if not result:
            abort(404, message="This username does not have any devices assigned")
        return result


class DeviceFull(Resource):
    """Supports GET requests.
    GET reads data from SQL database.
        returns full list of attribute data for mathing id
        see "full_resource_fields" for attributes
    """

    @marshal_with(full_resource_fields)
    def get(self, device_id):
        result = DeviceModel.query.filter_by(id=device_id).first()
        if not result:
            abort(404, message="Could not find device with that serial number")
        return result


class DeviceControl(Resource):
    """Supports GET and PUT requests.
    GET reads data from SQL database.
        returns control data for mathing id
    PUT updates values in SQL database
        returns updated control data for mathing id
    see "control_resource_fields" for attributes
    """

    @marshal_with(control_resource_fields)
    def get(self, device_id):
        result = DeviceModel.query.filter_by(id=device_id).first()
        if not result:
            abort(404, message="Could not find device with that id number")
        return result

    @marshal_with(control_resource_fields)
    def patch(self, device_id):
        args = device_update_args.parse_args()
        result = DeviceModel.query.filter_by(id=device_id).first()
        if not result:
            abort(404, message="Device doesn't exist, cannot update")

        if args["signal_type"]:
            result.signal_type = args["signal_type"]
        if args["signal_range_low"]:
            result.signal_range_low = args["signal_range_low"]
        if args["signal_range_high"]:
            result.signal_range_high = args["signal_range_high"]
        if args["flow_limit"]:
            result.flow_limit = args["flow_limit"]
        if args["pressure_controller"]:
            result.pressure_controller = args["pressure_controller"]

        db.session.commit()

        return result


class DeviceHistory(Resource):
    """Supports GET request. Generates random data for testing.
    Requires device_id, timeframe, attribute, and data_points
    Returns key value pair Attribute:[list of random ints, length =data_points]
    """

    def get(self, device_id, timeframe, attribute, data_points):
        result = {
            "device_id": device_id,
            "timeframe": timeframe,
            "attribute": attribute,
            "data_points": data_points,
        }
        good_attributes = [
            "temp",
            "operating_hours",
            "analogue_in",
            "spool_position",
            "pressure",
            "flow_torque",
            "uptime",
            "cycles",
            "issues",
        ]
        max_returned_data_points = 31
        # check request errors
        if not device_id:
            abort(404, message="Please provide a device id")

        if not timeframe:
            abort(404, message="Please provide a timeframe (week or month)")

        if not attribute:
            abort(404, message="Please provide an attribute to query")
        elif attribute not in good_attributes:
            abort(
                404,
                message="Please request one of the available attributes: "
                + str(good_attributes),
            )

        if not data_points:
            abort(404, message="Please provide the number of points you require")
        elif data_points > max_returned_data_points:
            abort(
                400,
                message="Please request a number of points less than or equal to: "
                + str(max_returned_data_points),
            )

        # generate random data
        values = random.sample(range(30), data_points)
        result = {str(attribute): values}

        # catch error or missing data
        if not result:
            abort(
                404,
                message="Could not find data on the device with the serial number provided",
            )
        return result


api.add_resource(
    Device,
    "/device/<string:user_id>",
)
api.add_resource(
    DeviceFull,
    "/device/full/<int:device_id>",
)
api.add_resource(
    DeviceHistory,
    "/device/history/<int:device_id>,<string:timeframe>,<string:attribute>,<int:data_points>",
)
api.add_resource(
    DeviceControl,
    "/device/control/<int:device_id>",
)

if __name__ == "__main__":
    app.run(debug=True)
