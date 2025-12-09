"""
악보 생성 테스트 스크립트
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_modules():
    """필수 모듈 로드 테스트"""
    print("=" * 60)
    print("필수 모듈 로드 테스트")
    print("=" * 60)
    
    try:
        from audio_processor import AudioProcessor
        print("[OK] AudioProcessor 로드 성공")
        ap = AudioProcessor()
        print(f"[OK] AudioProcessor 인스턴스 생성 성공")
        
        # basic-pitch 모델 로드 테스트
        predict = ap._load_basic_pitch_model()
        if predict:
            print("[OK] basic-pitch 모델 로드 성공")
        else:
            print("[ERROR] basic-pitch 모델 로드 실패")
            return False
    except Exception as e:
        print(f"[ERROR] AudioProcessor 로드 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    try:
        from score_processor import ScoreProcessor
        print("[OK] ScoreProcessor 로드 성공")
        sp = ScoreProcessor()
        print(f"[OK] ScoreProcessor 인스턴스 생성 성공")
    except Exception as e:
        print(f"[ERROR] ScoreProcessor 로드 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    try:
        from chord_generator import ChordGenerator
        print("[OK] ChordGenerator 로드 성공")
        cg = ChordGenerator()
        print(f"[OK] ChordGenerator 인스턴스 생성 성공")
    except Exception as e:
        print(f"[ERROR] ChordGenerator 로드 실패: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    try:
        from music21 import converter, stream
        print("[OK] music21 로드 성공")
    except Exception as e:
        print(f"[ERROR] music21 로드 실패: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("[결과] 모든 필수 모듈이 정상적으로 로드되었습니다!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_modules()
    sys.exit(0 if success else 1)

