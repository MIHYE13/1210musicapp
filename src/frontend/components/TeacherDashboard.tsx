import { useState, useEffect } from 'react'
import './TeacherDashboard.css'
import { db, ClassData, StudentData, ActivityData } from '../utils/storage'

const TeacherDashboard = () => {
  const [activePage, setActivePage] = useState<'home' | 'classes' | 'students' | 'activities' | 'statistics'>('home')
  const [classes, setClasses] = useState<ClassData[]>([])
  const [students, setStudents] = useState<StudentData[]>([])
  const [activities, setActivities] = useState<ActivityData[]>([])
  
  // Form states
  const [newClass, setNewClass] = useState({ grade: 1, classNumber: 1, className: '', teacherName: '' })
  const [selectedClassId, setSelectedClassId] = useState<string>('')
  const [newStudent, setNewStudent] = useState({ studentName: '', studentNumber: 1, notes: '' })
  const [newActivity, setNewActivity] = useState({
    activityDate: new Date().toISOString().split('T')[0],
    activityType: '수업',
    songTitle: '',
    description: '',
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = () => {
    setClasses(db.getClasses())
    setStudents(db.getStudents())
    setActivities(db.getActivities())
  }

  const handleAddClass = () => {
    if (!newClass.teacherName.trim()) {
      alert('담임 교사 이름을 입력해주세요.')
      return
    }
    db.addClass(newClass.grade, newClass.classNumber, newClass.className || undefined, newClass.teacherName)
    setNewClass({ grade: 1, classNumber: 1, className: '', teacherName: '' })
    loadData()
    alert('학급이 등록되었습니다!')
  }

  const handleDeleteClass = (classId: string) => {
    if (confirm('정말로 이 학급을 삭제하시겠습니까? 관련된 모든 학생과 활동 기록도 삭제됩니다.')) {
      db.deleteClass(classId)
      loadData()
      alert('학급이 삭제되었습니다.')
    }
  }

  const handleAddStudent = () => {
    if (!selectedClassId) {
      alert('학급을 선택해주세요.')
      return
    }
    if (!newStudent.studentName.trim()) {
      alert('학생 이름을 입력해주세요.')
      return
    }
    db.addStudent(selectedClassId, newStudent.studentName, newStudent.studentNumber, newStudent.notes || undefined)
    setNewStudent({ studentName: '', studentNumber: 1, notes: '' })
    loadData()
    alert('학생이 등록되었습니다!')
  }

  const handleDeleteStudent = (studentId: string) => {
    if (confirm('정말로 이 학생을 삭제하시겠습니까?')) {
      db.deleteStudent(studentId)
      loadData()
      alert('학생이 삭제되었습니다.')
    }
  }

  const handleAddActivity = () => {
    if (!selectedClassId) {
      alert('학급을 선택해주세요.')
      return
    }
    db.addActivity(
      selectedClassId,
      newActivity.activityDate,
      newActivity.activityType,
      newActivity.songTitle || undefined,
      newActivity.description || undefined
    )
    setNewActivity({
      activityDate: new Date().toISOString().split('T')[0],
      activityType: '수업',
      songTitle: '',
      description: '',
    })
    loadData()
    alert('활동이 기록되었습니다!')
  }

  const handleDeleteActivity = (activityId: string) => {
    if (confirm('정말로 이 활동을 삭제하시겠습니까?')) {
      db.deleteActivity(activityId)
      loadData()
      alert('활동이 삭제되었습니다.')
    }
  }

  const selectedClassStudents = selectedClassId ? db.getStudents(selectedClassId) : []
  const selectedClassActivities = selectedClassId ? db.getActivities(selectedClassId) : []

  // Statistics
  const totalStudents = students.length
  const totalActivities = activities.length
  const avgStudentsPerClass = classes.length > 0 ? (totalStudents / classes.length).toFixed(1) : '0'

  return (
    <div className="teacher-dashboard">
      <h2>👨‍🏫 교사용 대시보드</h2>

      <div className="dashboard-nav">
        <button
          className={`nav-btn ${activePage === 'home' ? 'active' : ''}`}
          onClick={() => setActivePage('home')}
        >
          📊 대시보드 홈
        </button>
        <button
          className={`nav-btn ${activePage === 'classes' ? 'active' : ''}`}
          onClick={() => setActivePage('classes')}
        >
          🏫 학급 관리
        </button>
        <button
          className={`nav-btn ${activePage === 'students' ? 'active' : ''}`}
          onClick={() => setActivePage('students')}
        >
          👥 학생 관리
        </button>
        <button
          className={`nav-btn ${activePage === 'activities' ? 'active' : ''}`}
          onClick={() => setActivePage('activities')}
        >
          📅 수업 기록
        </button>
        <button
          className={`nav-btn ${activePage === 'statistics' ? 'active' : ''}`}
          onClick={() => setActivePage('statistics')}
        >
          📈 통계 및 리포트
        </button>
      </div>

      <div className="dashboard-content">
        {activePage === 'home' && (
          <div className="section">
            <h3>📊 대시보드 개요</h3>
            {classes.length === 0 ? (
              <div className="info-box">
                <p>👋 학급을 먼저 등록하세요! '🏫 학급 관리'를 선택하세요.</p>
              </div>
            ) : (
              <>
                <div className="stats-grid">
                  <div className="stat-card">
                    <h4>전체 학급 수</h4>
                    <p className="stat-value">{classes.length}</p>
                  </div>
                  <div className="stat-card">
                    <h4>전체 학생 수</h4>
                    <p className="stat-value">{totalStudents}</p>
                  </div>
                  <div className="stat-card">
                    <h4>총 수업 기록</h4>
                    <p className="stat-value">{totalActivities}</p>
                  </div>
                  <div className="stat-card">
                    <h4>학급당 평균 인원</h4>
                    <p className="stat-value">{avgStudentsPerClass}명</p>
                  </div>
                </div>
                <div className="class-list">
                  <h4>📋 학급 목록</h4>
                  {classes.map((cls) => {
                    const classStudents = db.getStudents(cls.id)
                    const classActivities = db.getActivities(cls.id)
                    return (
                      <div key={cls.id} className="class-item">
                        <h5>
                          {cls.grade}학년 {cls.classNumber}반
                          {cls.className && ` - ${cls.className}`}
                        </h5>
                        <div className="class-info">
                          <p><strong>담임 교사:</strong> {cls.teacherName || '미지정'}</p>
                          <p><strong>학생 수:</strong> {classStudents.length}명</p>
                          <p><strong>수업 기록:</strong> {classActivities.length}회</p>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </>
            )}
          </div>
        )}

        {activePage === 'classes' && (
          <div className="section">
            <h3>🏫 학급 관리</h3>
            <div className="form-section">
              <h4>➕ 학급 추가</h4>
              <div className="form-row">
                <div className="form-group">
                  <label>학년</label>
                  <input
                    type="number"
                    className="form-control"
                    min={1}
                    max={6}
                    value={newClass.grade}
                    onChange={(e) => setNewClass({ ...newClass, grade: parseInt(e.target.value) })}
                  />
                </div>
                <div className="form-group">
                  <label>반</label>
                  <input
                    type="number"
                    className="form-control"
                    min={1}
                    max={20}
                    value={newClass.classNumber}
                    onChange={(e) => setNewClass({ ...newClass, classNumber: parseInt(e.target.value) })}
                  />
                </div>
                <div className="form-group">
                  <label>학급 이름 (선택)</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="예: 해바라기반"
                    value={newClass.className}
                    onChange={(e) => setNewClass({ ...newClass, className: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>담임 교사 *</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="예: 홍길동"
                    value={newClass.teacherName}
                    onChange={(e) => setNewClass({ ...newClass, teacherName: e.target.value })}
                  />
                </div>
              </div>
              <button className="action-button" onClick={handleAddClass}>
                ✅ 학급 등록
              </button>
            </div>

            <div className="list-section">
              <h4>📋 등록된 학급</h4>
              {classes.length === 0 ? (
                <p className="empty-message">등록된 학급이 없습니다.</p>
              ) : (
                <div className="table-container">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>학년</th>
                        <th>반</th>
                        <th>학급명</th>
                        <th>담임교사</th>
                        <th>작업</th>
                      </tr>
                    </thead>
                    <tbody>
                      {classes.map((cls) => (
                        <tr key={cls.id}>
                          <td>{cls.grade}</td>
                          <td>{cls.classNumber}</td>
                          <td>{cls.className || '-'}</td>
                          <td>{cls.teacherName || '-'}</td>
                          <td>
                            <button
                              className="delete-button"
                              onClick={() => handleDeleteClass(cls.id)}
                            >
                              🗑️ 삭제
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {activePage === 'students' && (
          <div className="section">
            <h3>👥 학생 관리</h3>
            {classes.length === 0 ? (
              <div className="info-box">
                <p>먼저 학급을 등록하세요!</p>
              </div>
            ) : (
              <>
                <div className="form-group">
                  <label>학급 선택</label>
                  <select
                    className="form-control"
                    value={selectedClassId}
                    onChange={(e) => setSelectedClassId(e.target.value)}
                  >
                    <option value="">학급을 선택하세요</option>
                    {classes.map((cls) => (
                      <option key={cls.id} value={cls.id}>
                        {cls.grade}학년 {cls.classNumber}반
                        {cls.className && ` - ${cls.className}`}
                      </option>
                    ))}
                  </select>
                </div>

                {selectedClassId && (
                  <>
                    <div className="form-section">
                      <h4>➕ 학생 추가</h4>
                      <div className="form-row">
                        <div className="form-group">
                          <label>학생 이름 *</label>
                          <input
                            type="text"
                            className="form-control"
                            placeholder="예: 김철수"
                            value={newStudent.studentName}
                            onChange={(e) => setNewStudent({ ...newStudent, studentName: e.target.value })}
                          />
                        </div>
                        <div className="form-group">
                          <label>번호</label>
                          <input
                            type="number"
                            className="form-control"
                            min={1}
                            max={50}
                            value={newStudent.studentNumber}
                            onChange={(e) => setNewStudent({ ...newStudent, studentNumber: parseInt(e.target.value) })}
                          />
                        </div>
                        <div className="form-group">
                          <label>특이사항 (선택)</label>
                          <textarea
                            className="form-control"
                            placeholder="악기 특성, 주의사항 등"
                            value={newStudent.notes}
                            onChange={(e) => setNewStudent({ ...newStudent, notes: e.target.value })}
                            rows={2}
                          />
                        </div>
                      </div>
                      <button className="action-button" onClick={handleAddStudent}>
                        ✅ 학생 등록
                      </button>
                    </div>

                    <div className="list-section">
                      <h4>📋 학생 명단</h4>
                      {selectedClassStudents.length === 0 ? (
                        <p className="empty-message">등록된 학생이 없습니다.</p>
                      ) : (
                        <div className="table-container">
                          <table className="data-table">
                            <thead>
                              <tr>
                                <th>번호</th>
                                <th>이름</th>
                                <th>특이사항</th>
                                <th>작업</th>
                              </tr>
                            </thead>
                            <tbody>
                              {selectedClassStudents.map((student) => (
                                <tr key={student.id}>
                                  <td>{student.studentNumber}</td>
                                  <td>{student.studentName}</td>
                                  <td>{student.notes || '-'}</td>
                                  <td>
                                    <button
                                      className="delete-button"
                                      onClick={() => handleDeleteStudent(student.id)}
                                    >
                                      🗑️ 삭제
                                    </button>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  </>
                )}
              </>
            )}
          </div>
        )}

        {activePage === 'activities' && (
          <div className="section">
            <h3>📅 수업 기록</h3>
            {classes.length === 0 ? (
              <div className="info-box">
                <p>먼저 학급을 등록하세요!</p>
              </div>
            ) : (
              <>
                <div className="form-group">
                  <label>학급 선택</label>
                  <select
                    className="form-control"
                    value={selectedClassId}
                    onChange={(e) => setSelectedClassId(e.target.value)}
                  >
                    <option value="">학급을 선택하세요</option>
                    {classes.map((cls) => (
                      <option key={cls.id} value={cls.id}>
                        {cls.grade}학년 {cls.classNumber}반
                        {cls.className && ` - ${cls.className}`}
                      </option>
                    ))}
                  </select>
                </div>

                {selectedClassId && (
                  <>
                    <div className="form-section">
                      <h4>➕ 활동 추가</h4>
                      <div className="form-row">
                        <div className="form-group">
                          <label>날짜</label>
                          <input
                            type="date"
                            className="form-control"
                            value={newActivity.activityDate}
                            onChange={(e) => setNewActivity({ ...newActivity, activityDate: e.target.value })}
                          />
                        </div>
                        <div className="form-group">
                          <label>활동 유형</label>
                          <select
                            className="form-control"
                            value={newActivity.activityType}
                            onChange={(e) => setNewActivity({ ...newActivity, activityType: e.target.value })}
                          >
                            <option>수업</option>
                            <option>연주회</option>
                            <option>평가</option>
                            <option>실기</option>
                            <option>감상</option>
                            <option>기타</option>
                          </select>
                        </div>
                        <div className="form-group">
                          <label>곡 제목</label>
                          <input
                            type="text"
                            className="form-control"
                            placeholder="예: 학교종"
                            value={newActivity.songTitle}
                            onChange={(e) => setNewActivity({ ...newActivity, songTitle: e.target.value })}
                          />
                        </div>
                      </div>
                      <div className="form-group">
                        <label>활동 내용</label>
                        <textarea
                          className="form-control"
                          placeholder="수업 내용, 학습 목표, 특이사항 등을 기록하세요."
                          value={newActivity.description}
                          onChange={(e) => setNewActivity({ ...newActivity, description: e.target.value })}
                          rows={4}
                        />
                      </div>
                      <button className="action-button" onClick={handleAddActivity}>
                        ✅ 기록 저장
                      </button>
                    </div>

                    <div className="list-section">
                      <h4>📋 활동 이력</h4>
                      {selectedClassActivities.length === 0 ? (
                        <p className="empty-message">기록된 활동이 없습니다.</p>
                      ) : (
                        <div className="activities-list">
                          {selectedClassActivities.map((activity) => (
                            <div key={activity.id} className="activity-item">
                              <div className="activity-header">
                                <h5>
                                  {activity.activityDate} - {activity.activityType}
                                  {activity.songTitle && `: ${activity.songTitle}`}
                                </h5>
                                <button
                                  className="delete-button"
                                  onClick={() => handleDeleteActivity(activity.id)}
                                >
                                  🗑️ 삭제
                                </button>
                              </div>
                              {activity.description && (
                                <p className="activity-description">{activity.description}</p>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </>
                )}
              </>
            )}
          </div>
        )}

        {activePage === 'statistics' && (
          <div className="section">
            <h3>📈 통계 및 리포트</h3>
            {classes.length === 0 ? (
              <div className="info-box">
                <p>먼저 학급을 등록하세요!</p>
              </div>
            ) : (
              <>
                <div className="stats-grid">
                  <div className="stat-card">
                    <h4>전체 학급</h4>
                    <p className="stat-value">{classes.length}</p>
                  </div>
                  <div className="stat-card">
                    <h4>전체 학생</h4>
                    <p className="stat-value">{totalStudents}</p>
                  </div>
                  <div className="stat-card">
                    <h4>전체 활동</h4>
                    <p className="stat-value">{totalActivities}</p>
                  </div>
                </div>
                <div className="class-list">
                  <h4>학급별 요약</h4>
                  {classes.map((cls) => {
                    const classStudents = db.getStudents(cls.id)
                    const classActivities = db.getActivities(cls.id)
                    return (
                      <div key={cls.id} className="class-item">
                        <h5>
                          {cls.grade}학년 {cls.classNumber}반
                          {cls.className && ` - ${cls.className}`}
                        </h5>
                        <div className="class-info">
                          <p><strong>학생수:</strong> {classStudents.length}명</p>
                          <p><strong>활동수:</strong> {classActivities.length}회</p>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default TeacherDashboard
