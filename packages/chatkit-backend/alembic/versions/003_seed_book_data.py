"""Seed book structure data from curriculum

Revision ID: 003_seed_book_data
Revises: 002_book_structure
Create Date: 2025-11-30

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '003_seed_book_data'
down_revision: Union[str, None] = '002_book_structure'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed the book structure from curriculum.md."""
    # Generate UUIDs for all entities
    book_id = str(uuid4())

    # Part UUIDs
    part_ids = [str(uuid4()) for _ in range(6)]

    # Chapter UUIDs (18 chapters)
    chapter_ids = [str(uuid4()) for _ in range(18)]

    # Insert book using raw SQL with UUID literals
    op.execute(
        sa.text(f"""
            INSERT INTO books (id, slug, title, description, version)
            VALUES (
                '{book_id}'::uuid,
                'ai-native-robotics',
                'Physical AI & Humanoid Robotics',
                'A comprehensive textbook for learning robotics with AI-native approaches. Bridging the gap between the digital brain and the physical body.',
                '1.0.0'
            )
        """)
    )

    # Insert parts
    parts_data = [
        (part_ids[0], 1, 'Physical AI Foundations', 'L1', 'A2', '01-Physical-AI-Foundations', 1, 2),
        (part_ids[1], 2, 'ROS 2 Fundamentals', 'L2-L3', 'B1', '02-ROS2-Fundamentals', 3, 5),
        (part_ids[2], 3, 'Simulation Systems', 'L2', 'B2', '03-Simulation-Systems', 6, 7),
        (part_ids[3], 4, 'NVIDIA Isaac Robotics AI', 'L2-L3', 'C1', '04-NVIDIA-Isaac-AI', 8, 10),
        (part_ids[4], 5, 'Vision-Language-Action', 'L4', 'C2', '05-Vision-Language-Action', 11, 12),
        (part_ids[5], 6, 'Capstone Project', 'L5', 'C2', '06-Capstone', 13, 13),
    ]

    for part_id, number, title, layer, tier, folder_name, week_start, week_end in parts_data:
        # Escape single quotes in title
        title_escaped = title.replace("'", "''")
        op.execute(
            sa.text(f"""
                INSERT INTO parts (id, book_id, number, title, layer, tier, folder_name, week_start, week_end)
                VALUES ('{part_id}'::uuid, '{book_id}'::uuid, {number}, '{title_escaped}', '{layer}', '{tier}', '{folder_name}', {week_start}, {week_end})
            """)
        )

    # Insert chapters
    chapters_data = [
        # Part 1: Physical AI Foundations (Chapters 1-3)
        (chapter_ids[0], part_ids[0], 1, 1, 'What Is Physical AI? The Rise of Embodied Intelligence', '01-what-is-physical-ai', None),
        (chapter_ids[1], part_ids[0], 2, 2, 'Sensors, Actuators & The Humanoid Body Plan', '02-sensors-actuators-humanoid-body', [chapter_ids[0]]),
        (chapter_ids[2], part_ids[0], 3, 3, 'The Humanoid Robotics Landscape', '03-humanoid-robotics-landscape', [chapter_ids[0]]),

        # Part 2: ROS 2 Fundamentals (Chapters 4-7)
        (chapter_ids[3], part_ids[1], 4, 1, 'ROS 2 Architecture', '04-ros2-architecture', [chapter_ids[2]]),
        (chapter_ids[4], part_ids[1], 5, 2, 'Creating ROS 2 Packages with Python', '05-ros2-packages-with-python', [chapter_ids[3]]),
        (chapter_ids[5], part_ids[1], 6, 3, 'URDF for Humanoids', '06-urdf-for-humanoids', [chapter_ids[3]]),
        (chapter_ids[6], part_ids[1], 7, 4, 'Bridging AI Agents to ROS 2', '07-ai-agent-ros2-bridge', [chapter_ids[4], chapter_ids[5]]),

        # Part 3: Simulation Systems (Chapters 8-11)
        (chapter_ids[7], part_ids[2], 8, 1, 'Digital Twins', '08-digital-twins-simulation', [chapter_ids[5]]),
        (chapter_ids[8], part_ids[2], 9, 2, 'Gazebo Simulation', '09-gazebo-simulation', [chapter_ids[7]]),
        (chapter_ids[9], part_ids[2], 10, 3, 'Unity for Robotics', '10-unity-for-robotics', [chapter_ids[7]]),
        (chapter_ids[10], part_ids[2], 11, 4, 'Sensor Simulation', '11-sensor-simulation', [chapter_ids[8]]),

        # Part 4: NVIDIA Isaac (Chapters 12-14)
        (chapter_ids[11], part_ids[3], 12, 1, 'Isaac Sim Fundamentals', '12-isaac-sim-fundamentals', [chapter_ids[8]]),
        (chapter_ids[12], part_ids[3], 13, 2, 'Isaac ROS Perception', '13-isaac-ros-perception', [chapter_ids[11]]),
        (chapter_ids[13], part_ids[3], 14, 3, 'Nav2 for Humanoids', '14-nav2-humanoid-path-planning', [chapter_ids[12]]),

        # Part 5: Vision-Language-Action (Chapters 15-17)
        (chapter_ids[14], part_ids[4], 15, 1, 'Whisper for Voice-to-Action', '15-whisper-voice-to-action', [chapter_ids[6]]),
        (chapter_ids[15], part_ids[4], 16, 2, 'Cognitive Planning', '16-cognitive-planning-llm-to-ros2', [chapter_ids[14]]),
        (chapter_ids[16], part_ids[4], 17, 3, 'Multimodal Perception', '17-multimodal-perception-humanoid', [chapter_ids[15]]),

        # Part 6: Capstone (Chapter 18)
        (chapter_ids[17], part_ids[5], 18, 1, 'Build an Autonomous Humanoid Robot', '18-capstone-autonomous-humanoid', [chapter_ids[13], chapter_ids[16]]),
    ]

    for chapter_id, part_id, number, local_number, title, folder_name, prerequisites in chapters_data:
        prereqs_json = 'null' if prerequisites is None else str(prerequisites).replace("'", '"')
        title_escaped = title.replace("'", "''")
        op.execute(
            sa.text(f"""
                INSERT INTO chapters (id, part_id, number, local_number, title, folder_name, prerequisites)
                VALUES ('{chapter_id}'::uuid, '{part_id}'::uuid, {number}, {local_number}, '{title_escaped}', '{folder_name}', '{prereqs_json}'::jsonb)
            """)
        )

    # Insert lessons for Part 1 (the only part with written content)
    lessons_data = [
        # Chapter 1: What Is Physical AI?
        (chapter_ids[0], 1, 'Digital AI vs Physical AI', 'ch01-digital-vs-physical-ai', 'lesson'),
        (chapter_ids[0], 2, 'The Embodiment Hypothesis', 'ch01-embodiment-hypothesis', 'lesson'),
        (chapter_ids[0], 3, 'Real-world Constraints', 'ch01-real-world-constraints', 'lesson'),
        (chapter_ids[0], 4, 'Lab: Try With AI', 'ch01-lab', 'lab'),

        # Chapter 2: Sensors, Actuators & The Humanoid Body Plan
        (chapter_ids[1], 1, 'How Robots Sense', 'ch02-how-robots-sense', 'lesson'),
        (chapter_ids[1], 2, 'Actuators and Movement', 'ch02-actuators-and-movement', 'lesson'),
        (chapter_ids[1], 3, 'The Humanoid Body Plan', 'ch02-humanoid-body-plan', 'lesson'),
        (chapter_ids[1], 4, 'Lab: Sensor Identification', 'ch02-lab', 'lab'),

        # Chapter 3: The Humanoid Robotics Landscape
        (chapter_ids[2], 1, 'Why Humanoid Form?', 'ch03-why-humanoid-form', 'lesson'),
        (chapter_ids[2], 2, 'Current Platforms', 'ch03-current-platforms', 'lesson'),
        (chapter_ids[2], 3, 'Challenges and Future Directions', 'ch03-challenges-future', 'lesson'),
        (chapter_ids[2], 4, 'Lab: Research Humanoid Robots', 'ch03-lab', 'lab'),
    ]

    for chapter_id, number, title, slug, type_ in lessons_data:
        lesson_id = str(uuid4())
        title_escaped = title.replace("'", "''")
        op.execute(
            sa.text(f"""
                INSERT INTO lessons (id, chapter_id, number, title, slug, type)
                VALUES ('{lesson_id}'::uuid, '{chapter_id}'::uuid, {number}, '{title_escaped}', '{slug}', '{type_}')
            """)
        )


def downgrade() -> None:
    """Remove all seeded data."""
    # Delete in reverse order of dependencies
    op.execute(sa.text("DELETE FROM lessons WHERE chapter_id IN (SELECT id FROM chapters WHERE part_id IN (SELECT id FROM parts WHERE book_id IN (SELECT id FROM books WHERE slug = 'ai-native-robotics')))"))
    op.execute(sa.text("DELETE FROM chapters WHERE part_id IN (SELECT id FROM parts WHERE book_id IN (SELECT id FROM books WHERE slug = 'ai-native-robotics'))"))
    op.execute(sa.text("DELETE FROM parts WHERE book_id IN (SELECT id FROM books WHERE slug = 'ai-native-robotics')"))
    op.execute(sa.text("DELETE FROM books WHERE slug = 'ai-native-robotics'"))
