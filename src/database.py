"""
Database Module
SQLite database for teacher dashboard functionality
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os

class DatabaseManager:
    """Manage SQLite database for teacher dashboard"""
    
    def __init__(self, db_path: str = "data/music_helper.db"):
        """Initialize database"""
        self.db_path = db_path
        
        # Create data directory if not exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Classes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grade INTEGER NOT NULL,
                class_number INTEGER NOT NULL,
                class_name TEXT,
                teacher_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(grade, class_number)
            )
        """)
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                student_name TEXT NOT NULL,
                student_number INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes(id)
            )
        """)
        
        # Activities table (수업/활동 기록)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                activity_date DATE NOT NULL,
                activity_type TEXT NOT NULL,
                song_title TEXT,
                description TEXT,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes(id)
            )
        """)
        
        # Student progress table (학생별 진도)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                activity_id INTEGER NOT NULL,
                progress_status TEXT,
                score INTEGER,
                notes TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (activity_id) REFERENCES activities(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    # Class Management
    
    def add_class(self, grade: int, class_number: int, 
                  class_name: str = "", teacher_name: str = "") -> int:
        """Add a new class"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO classes (grade, class_number, class_name, teacher_name)
                VALUES (?, ?, ?, ?)
            """, (grade, class_number, class_name, teacher_name))
            
            class_id = cursor.lastrowid
            conn.commit()
            return class_id
        except sqlite3.IntegrityError:
            # Class already exists
            cursor.execute("""
                SELECT id FROM classes WHERE grade = ? AND class_number = ?
            """, (grade, class_number))
            return cursor.fetchone()[0]
        finally:
            conn.close()
    
    def get_all_classes(self) -> List[Dict]:
        """Get all classes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, grade, class_number, class_name, teacher_name, created_at
            FROM classes
            ORDER BY grade, class_number
        """)
        
        classes = []
        for row in cursor.fetchall():
            classes.append({
                "id": row[0],
                "grade": row[1],
                "class_number": row[2],
                "class_name": row[3],
                "teacher_name": row[4],
                "created_at": row[5]
            })
        
        conn.close()
        return classes
    
    def get_class(self, class_id: int) -> Optional[Dict]:
        """Get a specific class"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, grade, class_number, class_name, teacher_name, created_at
            FROM classes
            WHERE id = ?
        """, (class_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "grade": row[1],
                "class_number": row[2],
                "class_name": row[3],
                "teacher_name": row[4],
                "created_at": row[5]
            }
        return None
    
    # Student Management
    
    def add_student(self, class_id: int, student_name: str, 
                   student_number: int = None, notes: str = "") -> int:
        """Add a new student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO students (class_id, student_name, student_number, notes)
            VALUES (?, ?, ?, ?)
        """, (class_id, student_name, student_number, notes))
        
        student_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return student_id
    
    def get_students_by_class(self, class_id: int) -> List[Dict]:
        """Get all students in a class"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, student_name, student_number, notes, created_at
            FROM students
            WHERE class_id = ?
            ORDER BY student_number, student_name
        """, (class_id,))
        
        students = []
        for row in cursor.fetchall():
            students.append({
                "id": row[0],
                "student_name": row[1],
                "student_number": row[2],
                "notes": row[3],
                "created_at": row[4]
            })
        
        conn.close()
        return students
    
    def update_student(self, student_id: int, student_name: str = None,
                      student_number: int = None, notes: str = None):
        """Update student information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if student_name is not None:
            updates.append("student_name = ?")
            params.append(student_name)
        if student_number is not None:
            updates.append("student_number = ?")
            params.append(student_number)
        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)
        
        if updates:
            params.append(student_id)
            cursor.execute(f"""
                UPDATE students
                SET {', '.join(updates)}
                WHERE id = ?
            """, params)
            conn.commit()
        
        conn.close()
    
    def delete_student(self, student_id: int):
        """Delete a student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
    
    # Activity Management
    
    def add_activity(self, class_id: int, activity_date: str, 
                    activity_type: str, song_title: str = "",
                    description: str = "", file_path: str = "") -> int:
        """Add a new activity/lesson"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO activities 
            (class_id, activity_date, activity_type, song_title, description, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (class_id, activity_date, activity_type, song_title, description, file_path))
        
        activity_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return activity_id
    
    def get_activities_by_class(self, class_id: int, 
                               start_date: str = None, 
                               end_date: str = None) -> List[Dict]:
        """Get activities for a class"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT id, activity_date, activity_type, song_title, 
                   description, file_path, created_at
            FROM activities
            WHERE class_id = ?
        """
        params = [class_id]
        
        if start_date:
            query += " AND activity_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND activity_date <= ?"
            params.append(end_date)
        
        query += " ORDER BY activity_date DESC"
        
        cursor.execute(query, params)
        
        activities = []
        for row in cursor.fetchall():
            activities.append({
                "id": row[0],
                "activity_date": row[1],
                "activity_type": row[2],
                "song_title": row[3],
                "description": row[4],
                "file_path": row[5],
                "created_at": row[6]
            })
        
        conn.close()
        return activities
    
    def delete_activity(self, activity_id: int):
        """Delete an activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
        conn.commit()
        conn.close()
    
    # Student Progress
    
    def record_progress(self, student_id: int, activity_id: int,
                       progress_status: str, score: int = None,
                       notes: str = "") -> int:
        """Record student progress for an activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO student_progress 
            (student_id, activity_id, progress_status, score, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, activity_id, progress_status, score, notes))
        
        progress_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return progress_id
    
    def get_student_progress(self, student_id: int) -> List[Dict]:
        """Get all progress records for a student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sp.id, a.activity_date, a.activity_type, a.song_title,
                   sp.progress_status, sp.score, sp.notes, sp.recorded_at
            FROM student_progress sp
            JOIN activities a ON sp.activity_id = a.id
            WHERE sp.student_id = ?
            ORDER BY a.activity_date DESC
        """, (student_id,))
        
        progress = []
        for row in cursor.fetchall():
            progress.append({
                "id": row[0],
                "activity_date": row[1],
                "activity_type": row[2],
                "song_title": row[3],
                "progress_status": row[4],
                "score": row[5],
                "notes": row[6],
                "recorded_at": row[7]
            })
        
        conn.close()
        return progress
    
    def get_class_statistics(self, class_id: int) -> Dict:
        """Get statistics for a class"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total students
        cursor.execute("""
            SELECT COUNT(*) FROM students WHERE class_id = ?
        """, (class_id,))
        total_students = cursor.fetchone()[0]
        
        # Total activities
        cursor.execute("""
            SELECT COUNT(*) FROM activities WHERE class_id = ?
        """, (class_id,))
        total_activities = cursor.fetchone()[0]
        
        # Average score
        cursor.execute("""
            SELECT AVG(sp.score)
            FROM student_progress sp
            JOIN students s ON sp.student_id = s.id
            WHERE s.class_id = ? AND sp.score IS NOT NULL
        """, (class_id,))
        avg_score = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_students": total_students,
            "total_activities": total_activities,
            "average_score": round(avg_score, 1)
        }
