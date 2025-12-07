"""
Teacher Dashboard Page
Manage classes, students, and track progress
"""

import streamlit as st
from database import DatabaseManager
from datetime import datetime, date
import pandas as pd

# Page config
st.set_page_config(
    page_title="교사용 대시보드",
    page_icon="👨‍🏫",
    layout="wide"
)

# Initialize database
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()

st.title("👨‍🏫 교사용 대시보드")
st.markdown("---")

# Sidebar for navigation
page = st.sidebar.selectbox(
    "메뉴",
    ["📊 대시보드 홈", "🏫 학급 관리", "👥 학생 관리", "📅 수업 기록", "📈 통계 및 리포트"]
)

# ============================================
# 대시보드 홈
# ============================================
if page == "📊 대시보드 홈":
    st.header("📊 대시보드 개요")
    
    # Get all classes
    classes = st.session_state.db.get_all_classes()
    
    if not classes:
        st.info("👋 학급을 먼저 등록하세요! 왼쪽 메뉴에서 '🏫 학급 관리'를 선택하세요.")
    else:
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("전체 학급 수", len(classes))
        
        with col2:
            total_students = sum(
                len(st.session_state.db.get_students_by_class(c['id'])) 
                for c in classes
            )
            st.metric("전체 학생 수", total_students)
        
        with col3:
            total_activities = sum(
                len(st.session_state.db.get_activities_by_class(c['id']))
                for c in classes
            )
            st.metric("총 수업 기록", total_activities)
        
        with col4:
            avg_students = total_students / len(classes) if classes else 0
            st.metric("학급당 평균 인원", f"{avg_students:.1f}명")
        
        st.markdown("---")
        
        # Class list with quick stats
        st.subheader("📋 학급 목록")
        
        for cls in classes:
            with st.expander(f"{cls['grade']}학년 {cls['class_number']}반" + 
                           (f" - {cls['class_name']}" if cls['class_name'] else "")):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**담임 교사**: {cls['teacher_name'] or '미지정'}")
                    students = st.session_state.db.get_students_by_class(cls['id'])
                    st.write(f"**학생 수**: {len(students)}명")
                
                with col2:
                    activities = st.session_state.db.get_activities_by_class(cls['id'])
                    st.write(f"**수업 기록**: {len(activities)}회")
                    stats = st.session_state.db.get_class_statistics(cls['id'])
                    if stats['average_score'] > 0:
                        st.write(f"**평균 점수**: {stats['average_score']}점")

# ============================================
# 학급 관리
# ============================================
elif page == "🏫 학급 관리":
    st.header("🏫 학급 관리")
    
    tab1, tab2 = st.tabs(["➕ 학급 추가", "📋 학급 목록"])
    
    with tab1:
        st.subheader("새 학급 등록")
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade = st.number_input("학년", min_value=1, max_value=6, value=1, step=1)
            class_number = st.number_input("반", min_value=1, max_value=20, value=1, step=1)
        
        with col2:
            class_name = st.text_input("학급 이름 (선택)", placeholder="예: 해바라기반")
            teacher_name = st.text_input("담임 교사", placeholder="예: 홍길동")
        
        if st.button("✅ 학급 등록", type="primary"):
            try:
                class_id = st.session_state.db.add_class(
                    grade, class_number, class_name, teacher_name
                )
                st.success(f"✅ {grade}학년 {class_number}반이 등록되었습니다!")
                st.rerun()
            except Exception as e:
                st.error(f"오류: {str(e)}")
    
    with tab2:
        st.subheader("등록된 학급")
        
        classes = st.session_state.db.get_all_classes()
        
        if not classes:
            st.info("등록된 학급이 없습니다.")
        else:
            # Display as table
            df = pd.DataFrame(classes)
            df = df[['grade', 'class_number', 'class_name', 'teacher_name']]
            df.columns = ['학년', '반', '학급명', '담임교사']
            
            st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================
# 학생 관리
# ============================================
elif page == "👥 학생 관리":
    st.header("👥 학생 관리")
    
    # Select class
    classes = st.session_state.db.get_all_classes()
    
    if not classes:
        st.warning("먼저 학급을 등록하세요!")
    else:
        class_options = {f"{c['grade']}학년 {c['class_number']}반": c['id'] for c in classes}
        selected_class = st.selectbox("학급 선택", list(class_options.keys()))
        class_id = class_options[selected_class]
        
        tab1, tab2 = st.tabs(["➕ 학생 추가", "📋 학생 목록"])
        
        with tab1:
            st.subheader("새 학생 등록")
            
            col1, col2 = st.columns(2)
            
            with col1:
                student_name = st.text_input("학생 이름", placeholder="예: 김철수")
                student_number = st.number_input("번호", min_value=1, max_value=50, value=1)
            
            with col2:
                notes = st.text_area("특이사항 (선택)", placeholder="악기 특성, 주의사항 등")
            
            if st.button("✅ 학생 등록", type="primary"):
                if student_name:
                    st.session_state.db.add_student(
                        class_id, student_name, student_number, notes
                    )
                    st.success(f"✅ {student_name} 학생이 등록되었습니다!")
                    st.rerun()
                else:
                    st.error("학생 이름을 입력하세요.")
        
        with tab2:
            st.subheader("학생 명단")
            
            students = st.session_state.db.get_students_by_class(class_id)
            
            if not students:
                st.info("등록된 학생이 없습니다.")
            else:
                # Display as table
                df = pd.DataFrame(students)
                df = df[['student_number', 'student_name', 'notes']]
                df.columns = ['번호', '이름', '특이사항']
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Download as CSV
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 명단 다운로드 (CSV)",
                    data=csv,
                    file_name=f"{selected_class}_명단.csv",
                    mime="text/csv"
                )
                
                # Edit/Delete students
                st.markdown("---")
                st.subheader("학생 정보 수정")
                
                student_to_edit = st.selectbox(
                    "수정할 학생",
                    [f"{s['student_number']}번 {s['student_name']}" for s in students]
                )
                
                if student_to_edit:
                    idx = int(student_to_edit.split("번")[0]) - 1
                    student = students[idx]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("이름", value=student['student_name'], key="edit_name")
                        new_number = st.number_input("번호", value=student['student_number'], key="edit_number")
                    
                    with col2:
                        new_notes = st.text_area("특이사항", value=student['notes'] or "", key="edit_notes")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button("💾 수정 저장"):
                            st.session_state.db.update_student(
                                student['id'], new_name, new_number, new_notes
                            )
                            st.success("✅ 저장되었습니다!")
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("🗑️ 학생 삭제", type="secondary"):
                            st.session_state.db.delete_student(student['id'])
                            st.success("✅ 삭제되었습니다!")
                            st.rerun()

# ============================================
# 수업 기록
# ============================================
elif page == "📅 수업 기록":
    st.header("📅 수업 기록")
    
    # Select class
    classes = st.session_state.db.get_all_classes()
    
    if not classes:
        st.warning("먼저 학급을 등록하세요!")
    else:
        class_options = {f"{c['grade']}학년 {c['class_number']}반": c['id'] for c in classes}
        selected_class = st.selectbox("학급 선택", list(class_options.keys()))
        class_id = class_options[selected_class]
        
        tab1, tab2, tab3 = st.tabs(["➕ 활동 추가", "📋 활동 목록", "✏️ 학생별 기록"])
        
        with tab1:
            st.subheader("새 수업/활동 기록")
            
            col1, col2 = st.columns(2)
            
            with col1:
                activity_date = st.date_input("날짜", value=date.today())
                activity_type = st.selectbox(
                    "활동 유형",
                    ["수업", "연주회", "평가", "실기", "감상", "기타"]
                )
            
            with col2:
                song_title = st.text_input("곡 제목", placeholder="예: 학교종")
                file_path = st.text_input("악보 파일 경로 (선택)", placeholder="예: /outputs/score.mid")
            
            description = st.text_area(
                "활동 내용",
                placeholder="수업 내용, 학습 목표, 특이사항 등을 기록하세요."
            )
            
            if st.button("✅ 기록 저장", type="primary"):
                st.session_state.db.add_activity(
                    class_id,
                    activity_date.strftime("%Y-%m-%d"),
                    activity_type,
                    song_title,
                    description,
                    file_path
                )
                st.success("✅ 활동이 기록되었습니다!")
                st.rerun()
        
        with tab2:
            st.subheader("활동 이력")
            
            # Date filter
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("시작 날짜", value=None)
            with col2:
                end_date = st.date_input("종료 날짜", value=None)
            
            activities = st.session_state.db.get_activities_by_class(
                class_id,
                start_date.strftime("%Y-%m-%d") if start_date else None,
                end_date.strftime("%Y-%m-%d") if end_date else None
            )
            
            if not activities:
                st.info("기록된 활동이 없습니다.")
            else:
                for activity in activities:
                    with st.expander(
                        f"{activity['activity_date']} - {activity['activity_type']}: {activity['song_title'] or '(제목 없음)'}"
                    ):
                        st.write(f"**내용**: {activity['description']}")
                        if activity['file_path']:
                            st.write(f"**파일**: {activity['file_path']}")
                        
                        if st.button(f"🗑️ 삭제", key=f"del_{activity['id']}"):
                            st.session_state.db.delete_activity(activity['id'])
                            st.success("✅ 삭제되었습니다!")
                            st.rerun()
        
        with tab3:
            st.subheader("학생별 진도 기록")
            
            students = st.session_state.db.get_students_by_class(class_id)
            activities = st.session_state.db.get_activities_by_class(class_id)
            
            if not students:
                st.info("먼저 학생을 등록하세요.")
            elif not activities:
                st.info("먼저 활동을 기록하세요.")
            else:
                # Select student and activity
                col1, col2 = st.columns(2)
                
                with col1:
                    student_options = {f"{s['student_number']}번 {s['student_name']}": s['id'] 
                                     for s in students}
                    selected_student = st.selectbox("학생 선택", list(student_options.keys()))
                    student_id = student_options[selected_student]
                
                with col2:
                    activity_options = {f"{a['activity_date']} - {a['song_title']}": a['id']
                                      for a in activities}
                    selected_activity = st.selectbox("활동 선택", list(activity_options.keys()))
                    activity_id = activity_options[selected_activity]
                
                # Record progress
                col1, col2 = st.columns(2)
                
                with col1:
                    progress_status = st.selectbox(
                        "진도 상태",
                        ["완료", "진행중", "미완료", "보충 필요"]
                    )
                    score = st.slider("점수", 0, 100, 80, 5)
                
                with col2:
                    progress_notes = st.text_area("메모", placeholder="학생의 연주 상태, 개선 사항 등")
                
                if st.button("✅ 진도 기록", type="primary"):
                    st.session_state.db.record_progress(
                        student_id, activity_id, progress_status, score, progress_notes
                    )
                    st.success("✅ 진도가 기록되었습니다!")
                
                # Show student progress history
                st.markdown("---")
                st.subheader(f"{selected_student} 학습 이력")
                
                progress = st.session_state.db.get_student_progress(student_id)
                
                if progress:
                    df = pd.DataFrame(progress)
                    df = df[['activity_date', 'song_title', 'progress_status', 'score']]
                    df.columns = ['날짜', '곡', '상태', '점수']
                    st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================
# 통계 및 리포트
# ============================================
elif page == "📈 통계 및 리포트":
    st.header("📈 통계 및 리포트")
    
    classes = st.session_state.db.get_all_classes()
    
    if not classes:
        st.warning("먼저 학급을 등록하세요!")
    else:
        # Class selection
        class_options = {f"{c['grade']}학년 {c['class_number']}반": c['id'] for c in classes}
        class_options["전체"] = None
        
        selected_class = st.selectbox("학급 선택", list(class_options.keys()))
        class_id = class_options[selected_class]
        
        if class_id is None:
            # Overall statistics
            st.subheader("📊 전체 통계")
            
            total_students = sum(
                len(st.session_state.db.get_students_by_class(c['id']))
                for c in classes
            )
            total_activities = sum(
                len(st.session_state.db.get_activities_by_class(c['id']))
                for c in classes
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("전체 학급", len(classes))
            with col2:
                st.metric("전체 학생", total_students)
            with col3:
                st.metric("전체 활동", total_activities)
            
            # Per-class summary
            st.markdown("---")
            st.subheader("학급별 요약")
            
            summary_data = []
            for cls in classes:
                stats = st.session_state.db.get_class_statistics(cls['id'])
                summary_data.append({
                    "학급": f"{cls['grade']}학년 {cls['class_number']}반",
                    "학생수": stats['total_students'],
                    "활동수": stats['total_activities'],
                    "평균점수": stats['average_score']
                })
            
            df = pd.DataFrame(summary_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
        else:
            # Single class statistics
            stats = st.session_state.db.get_class_statistics(class_id)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("학생 수", stats['total_students'])
            with col2:
                st.metric("활동 수", stats['total_activities'])
            with col3:
                st.metric("평균 점수", f"{stats['average_score']}점")
            
            # Recent activities
            st.markdown("---")
            st.subheader("최근 활동")
            
            activities = st.session_state.db.get_activities_by_class(class_id)
            if activities:
                recent = activities[:5]
                for act in recent:
                    st.write(f"• {act['activity_date']} - {act['activity_type']}: {act['song_title']}")
            else:
                st.info("활동 기록이 없습니다.")

# Footer
st.markdown("---")
st.markdown("**초등 음악 도우미** - 교사용 대시보드 📊")
