from shapely.geometry import Point, LineString, Polygon
from shapely import affinity
import math


from repos.spectra_analysis.fltool.data_processing.pptestlog import Testlog, Timestep, LogReader
from testing import testcase
from utils import calculation





class PPRuntime(object):
    def __init__(self):
        self.test_case = testcase.TestCase
        
        return



def get_speed_vector_ego():
    # return new Vector(speed * Math.cos(direction), speed * Math.sin(direction))
    return

def get_speed_vector_dynamic():
    return

def calculate_crash():
    return

def calculate_distance():
    return

def calculate_relative_speed():
    return

def calculate_danger():
    return

def calculate_max_danger_time(tstep, ego_state, dynamic_states):
    speed_vector_ego = calculation.BasicCalculation.get_vector_from_angle(ego_state['direction']) 
    danger_max = float('-inf') 
    for dynamic_state in dynamic_states:
        b_crash = calculate_crash(ego_state, dynamic_state)
        re_dis = calculate_distance(ego_state, dynamic_state)
        spd_vec_dynamic = get_speed_vector_dynamic(dynamic_state) 
        re_spd = calculate_relative_speed(speed_vector_ego) 
        danger = calculate_danger(re_dis, re_spd, b_crash)

# 这里需要定义一下runtimelog这个类 
def calculateMaximumDanger(runtimelog):
    maximumDanger = float('-inf')

    
    
    # (f egoTime : egoStatesByTime.keySet()) {
    #         CarState egoState = egoStatesByTime.get(egoTime);
    #         // the following is guaranteed to exist by ensureMatchingSizes()
    #         List<CarState> dynamicObjectStates = dynamicObjectStatesByTime.get(egoTime);
    #         Danger maxDangerAtThisTime = calculateMaximumDangerForTime(egoTime, egoState, dynamicObjectStates);
    #         if (maxDangerAtThisTime.bigger(maximumDanger)) {
    #             maximumDanger = maxDangerAtThisTime;
    #         }
    #     }
    #     return maximumDanger;
    # }


        
# * private Danger calculateMaximumDangerForTime(double time, CarState egoState, List<CarState> dynamicObjects) {
#         Danger maxDanger = null;

#         logger.log(Level.FINER, "t: " + time);
#         logger.log(Level.FINER, "   Ego  at " + egoState.getCenter() + " (v = " + egoState.getSpeedVector().getMagnitude() + ")");

#         Vector egoSpeedVector = egoState.getSpeedVector(); # 获取速度向量

#         for (int index = 0; index < dynamicObjects.size(); index++) {  # 遍历每一个dynamic
#             CarState dynamicObjectState = dynamicObjects.get(index);

#             boolean crashed = dynamicObjectState.crash(egoState);  # 判断是否crash

#             double distance = dynamicObjectState.distance(egoState);  # 判断距离

#             Vector dynamicObjectSpeedVector = dynamicObjectState.getSpeedVector();  # 获取dynamic的速度向量
#             double relativeSpeed = dynamicObjectSpeedVector.subtract(egoSpeedVector).getMagnitude();  # 获取相对速度
#             Danger danger = new Danger(distance, relativeSpeed, crashed);  # 


#             logger.log(Level.FINER, "   DO " + index + " at " + dynamicObjectState.getCenter() + "(v = " + dynamicObjectState.getSpeedVector().getMagnitude() + ") => d = " + distance + ", s = " + relativeSpeed + (dynamicObjectState.crash(egoState) ? " (crash!)" : ""));
#             if (danger.bigger(maxDanger)) {
#                 maxDanger = danger;
#             }
#         }
#         logger.log(Level.FINER, "   danger: " + maxDanger + " " + maxDanger.getMeasure());
#         return maxDanger;
#     }


# The state of each ego car and other cars
class CarState():
    def __init__(self, width:float=-1.0, length:float=-1.0, speed:float=-1.0,
        center:Point=Point([0, 0]), direction:float=math.pi/2, accelerationProfile:int=-1, 
        accleration:float=-1.0):
        self.width = width
        self.length = length
        self.speed = speed
        self.center =center
        self.direction = direction
        self.accelerationProfile = accelerationProfile
        self.accerleration = accleration

        return
    
    def scale_obj(self, factor:int):
        self.width *= factor 
        self.length *= factor 
        # setCenter(center.getX() * factor, center.getY() * factor); 按理说，center 应该是不变的啊

    def flip_y(self, height:float):
        set_center(self.center.x, height - self.center.y)
        self.direction = 2 * math.pi - direction
        return

    def set_center(self, x, y):
        self.center = Point(x, y)

    def cal_distance(self, other_car:CarState):
        dist = self.center.distance(other_car.center)
        return




    def get_shape(self):
        # 0 degree
        x = self.center.x
        y = self.center.y
        point1 = Point(x - self.length/2, y - self.height/2)
        point2 = Point(x + self.length/2, y - self.height/2)
        point3 = Point(x + self.length/2, y + self.height/2)
        point4 = Point(x - self.length/2, y + self.height/2)
        rect = Polygon([point1, point2, point3, point4])
        angle = self.direction * (180.0 / math.pi)
        rect = affinity.rotate(rect, angle)
        return rect
    

    def crash(self, other_car:CarState):
        rect_ego = self.get_shape()
        rect_other = rect_other.get_shape()
        intersection = rect_ego.intersection(rect_other)
        is_crash = not intersection.is_empty 
        return is_crash


#     public boolean crash(CarState other) {
#         Shape thisShape = this.getShape();
#         Shape otherShape = other.getShape();
#         if (thisShape.getBounds().intersects(otherShape.getBounds())) {
#             // only bother to calculate area intersection if bounding boxes intersect
#             Area area = new Area(thisShape);
#             area.intersect(new Area(otherShape));
#             // is there any area common to both shapes?
#             return !area.isEmpty();
#         }
#         // if bounding boxes don't intersect, the actual cars sure don't
#         return false;
#     }

#     /**
#      * Builds a rectangle that represents the actual state of the car, including rotation.
#      * This is how we are able to correctly calculate intersections.
#      *
#      * @return the shape of the car, in the correct size, position and rotation.
#      */
#     public Shape getShape() {
#         double x = center.getX();
#         double y = center.getY();
#         // Note on the last 2 parameters:
#         // a car positioned at 0° is horizontal (length is parallel to x axis). So a rectangle representing this car
#         // has width equal to the car length, and height equal to the car width.
#         Rectangle2D rect = new Rectangle2D.Double(x - length / 2, y - width / 2, length, width);
#         AffineTransform at = new AffineTransform();
#         at.rotate(direction, x, y);
#         return at.createTransformedShape(rect);
#     }

#     public Point getCenter() {
#         return center;
#     }

#     private void setCenter(double x, double y) {
#         this.center = new Point(x, y);
#     }

#     public Vector getSpeedVector() {
#         return new Vector(speed * Math.cos(direction), speed * Math.sin(direction));
#     }

#     @Override
#     public String toString() {
#         // approximate the angle to 1 decimal place, in order to easily get a nice representation
#         BigDecimal angle = BigDecimal.valueOf(direction / Math.PI).setScale(1, BigDecimal.ROUND_HALF_UP);
#         return "{ c = " + center + ", v = " + speed + ", Θ = " + formatAngle(angle) + " }";
#     }

#     /**
#      * Provides a human-readable representation of an angle (e.g. π/2, π, 0.75π).
#      *
#      * @param angle the angle, in radians.
#      * @return the representation string.
#      */
#     private String formatAngle(BigDecimal angle) {
#         if (angle.equals(new BigDecimal("0.0"))) return "0";
#         if (angle.equals(new BigDecimal("0.5"))) return "π/2";
#         if (angle.equals(new BigDecimal("1.0"))) return "π";
#         return angle.round(new MathContext(1)).toPlainString() + "π";
#     }

#     public String printFields() {
#         return center.getX() + "," + center.getY() + "," + direction + "," + speed + "," + accelerationProfile + "," + acceleration;
#     }
# }