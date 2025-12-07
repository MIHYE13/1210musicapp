// 로컬 스토리지 유틸리티

const STORAGE_PREFIX = 'music_app_'

export class Storage {
  private prefix: string

  constructor(prefix: string = STORAGE_PREFIX) {
    this.prefix = prefix
  }

  private getKey(key: string): string {
    return `${this.prefix}${key}`
  }

  set<T>(key: string, value: T): void {
    try {
      const serialized = JSON.stringify(value)
      localStorage.setItem(this.getKey(key), serialized)
    } catch (error) {
      console.error('Storage set error:', error)
    }
  }

  get<T>(key: string): T | null {
    try {
      const item = localStorage.getItem(this.getKey(key))
      if (item === null) return null
      return JSON.parse(item) as T
    } catch (error) {
      console.error('Storage get error:', error)
      return null
    }
  }

  remove(key: string): void {
    localStorage.removeItem(this.getKey(key))
  }

  clear(): void {
    const keys = Object.keys(localStorage)
    keys.forEach((key) => {
      if (key.startsWith(this.prefix)) {
        localStorage.removeItem(key)
      }
    })
  }
}

export const storage = new Storage()

// 특정 데이터 타입들
export interface ClassData {
  id: string
  grade: number
  classNumber: number
  className?: string
  teacherName?: string
  createdAt: string
}

export interface StudentData {
  id: string
  classId: string
  studentNumber: number
  studentName: string
  notes?: string
  createdAt: string
}

export interface ActivityData {
  id: string
  classId: string
  activityDate: string
  activityType: string
  songTitle?: string
  description?: string
  filePath?: string
  createdAt: string
}

export interface ProgressData {
  id: string
  studentId: string
  activityId: string
  progressStatus: string
  score: number
  notes?: string
  createdAt: string
}

// 데이터베이스 유틸리티
export class Database {
  private storage: Storage

  constructor() {
    this.storage = storage
  }

  // Classes
  getClasses(): ClassData[] {
    return this.storage.get<ClassData[]>('classes') || []
  }

  addClass(grade: number, classNumber: number, className?: string, teacherName?: string): string {
    const classes = this.getClasses()
    const newClass: ClassData = {
      id: `class_${Date.now()}`,
      grade,
      classNumber,
      className,
      teacherName,
      createdAt: new Date().toISOString(),
    }
    classes.push(newClass)
    this.storage.set('classes', classes)
    return newClass.id
  }

  deleteClass(classId: string): void {
    const classes = this.getClasses().filter((c) => c.id !== classId)
    this.storage.set('classes', classes)
    // 관련 학생과 활동도 삭제
    const students = this.getStudents().filter((s) => s.classId !== classId)
    this.storage.set('students', students)
    const activities = this.getActivities().filter((a) => a.classId !== classId)
    this.storage.set('activities', activities)
  }

  // Students
  getStudents(classId?: string): StudentData[] {
    const students = this.storage.get<StudentData[]>('students') || []
    if (classId) {
      return students.filter((s) => s.classId === classId)
    }
    return students
  }

  addStudent(classId: string, studentName: string, studentNumber: number, notes?: string): string {
    const students = this.getStudents()
    const newStudent: StudentData = {
      id: `student_${Date.now()}`,
      classId,
      studentName,
      studentNumber,
      notes,
      createdAt: new Date().toISOString(),
    }
    students.push(newStudent)
    this.storage.set('students', students)
    return newStudent.id
  }

  updateStudent(studentId: string, studentName: string, studentNumber: number, notes?: string): void {
    const students = this.getStudents()
    const index = students.findIndex((s) => s.id === studentId)
    if (index !== -1) {
      students[index] = { ...students[index], studentName, studentNumber, notes }
      this.storage.set('students', students)
    }
  }

  deleteStudent(studentId: string): void {
    const students = this.getStudents().filter((s) => s.id !== studentId)
    this.storage.set('students', students)
  }

  // Activities
  getActivities(classId?: string): ActivityData[] {
    const activities = this.storage.get<ActivityData[]>('activities') || []
    if (classId) {
      return activities.filter((a) => a.classId === classId)
    }
    return activities
  }

  addActivity(
    classId: string,
    activityDate: string,
    activityType: string,
    songTitle?: string,
    description?: string,
    filePath?: string
  ): string {
    const activities = this.getActivities()
    const newActivity: ActivityData = {
      id: `activity_${Date.now()}`,
      classId,
      activityDate,
      activityType,
      songTitle,
      description,
      filePath,
      createdAt: new Date().toISOString(),
    }
    activities.push(newActivity)
    this.storage.set('activities', activities)
    return newActivity.id
  }

  deleteActivity(activityId: string): void {
    const activities = this.getActivities().filter((a) => a.id !== activityId)
    this.storage.set('activities', activities)
  }

  // Progress
  getProgress(studentId?: string): ProgressData[] {
    const progress = this.storage.get<ProgressData[]>('progress') || []
    if (studentId) {
      return progress.filter((p) => p.studentId === studentId)
    }
    return progress
  }

  recordProgress(
    studentId: string,
    activityId: string,
    progressStatus: string,
    score: number,
    notes?: string
  ): string {
    const progress = this.getProgress()
    const newProgress: ProgressData = {
      id: `progress_${Date.now()}`,
      studentId,
      activityId,
      progressStatus,
      score,
      notes,
      createdAt: new Date().toISOString(),
    }
    progress.push(newProgress)
    this.storage.set('progress', progress)
    return newProgress.id
  }
}

export const db = new Database()

