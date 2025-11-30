# Technical Terms Glossary

## Terms to Preserve in English

### Robotics Terms

| English Term | Urdu Explanation (first use only) | Category |
|--------------|----------------------------------|----------|
| ROS 2 | روبوٹ آپریٹنگ سسٹم کا دوسرا ورژن | Platform |
| URDF | روبوٹ کی تفصیل کا فارمیٹ | Format |
| Gazebo | روبوٹ سمیولیشن سافٹ ویئر | Simulator |
| Isaac Sim | این ویڈیا کا سمیولیشن پلیٹ فارم | Simulator |
| node | ROS 2 میں چلنے والا پروگرام | ROS 2 |
| topic | پیغامات کا چینل | ROS 2 |
| publisher | پیغامات بھیجنے والا | ROS 2 |
| subscriber | پیغامات وصول کرنے والا | ROS 2 |
| message | ڈیٹا کا پیکٹ | ROS 2 |
| service | درخواست اور جواب | ROS 2 |
| action | لمبے عرصے کا کام | ROS 2 |
| launch file | متعدد نوڈز شروع کرنے کی فائل | ROS 2 |
| package | کوڈ کا مجموعہ | ROS 2 |
| workspace | پروجیکٹ فولڈر | ROS 2 |

### AI/ML Terms

| English Term | Urdu Explanation (first use only) | Category |
|--------------|----------------------------------|----------|
| AI | مصنوعی ذہانت | Core |
| machine learning | مشین لرننگ | Core |
| neural network | اعصابی نیٹ ورک | Core |
| model | تربیت یافتہ سسٹم | Core |
| training | ماڈل کی تربیت | Process |
| inference | پیشن گوئی | Process |
| dataset | ڈیٹا کا مجموعہ | Data |
| prompt | ہدایت نامہ | LLM |
| LLM | بڑا زبان ماڈل | LLM |
| embedding | عددی نمائندگی | LLM |
| RAG | بازیافت کے ساتھ جنریشن | LLM |

### Programming Terms

| English Term | Urdu Explanation (first use only) | Category |
|--------------|----------------------------------|----------|
| Python | پروگرامنگ زبان | Language |
| function | فنکشن | Code |
| class | کلاس | Code |
| variable | متغیر | Code |
| API | ایپلیکیشن انٹرفیس | Integration |
| JSON | ڈیٹا فارمیٹ | Format |
| YAML | کنفیگریشن فارمیٹ | Format |

### Hardware Terms

| English Term | Urdu Explanation (first use only) | Category |
|--------------|----------------------------------|----------|
| sensor | حسی آلہ | Component |
| actuator | عمل کرنے والا آلہ | Component |
| motor | موٹر | Component |
| joint | جوڑ | URDF |
| link | حصہ | URDF |
| lidar | لیزر سینسر | Sensor |
| IMU | حرکت کا سینسر | Sensor |
| camera | کیمرہ | Sensor |
| GPU | گرافکس پروسیسر | Hardware |

## Never Translate

These should NEVER be translated or explained:

- File names: `robot.urdf`, `config.yaml`
- Commands: `ros2 run`, `colcon build`
- Code: `def main():`, `import rclpy`
- Package names: `sensor_msgs`, `geometry_msgs`
- Error messages: Keep in English
- URLs and paths

## Translation Examples

### Good Translation

**English**:
> "Create a ROS 2 node that publishes sensor data."

**Urdu**:
> "ایک ROS 2 (روبوٹ آپریٹنگ سسٹم) node بنائیں جو sensor data publish کرے۔"

### Bad Translation

**English**:
> "Create a ROS 2 node that publishes sensor data."

**Urdu (WRONG)**:
> "ایک روس ٹو نوڈ بنائیں جو سینسر ڈیٹا شائع کرے۔"

(Technical terms should remain in English!)
