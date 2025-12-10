"""
OMR (Optical Music Recognition) Service
이미지를 MusicXML로 변환하는 OMR 서비스
"""
import subprocess
from pathlib import Path
import tempfile
from typing import Union


class OmrError(Exception):
    """OMR 관련 오류"""
    pass


class AudiverisOmr:
    """Audiveris를 사용한 OMR 서비스"""
    
    def __init__(self, audiveris_bin: Union[str, Path]):
        """
        Audiveris OMR 서비스 초기화
        
        Args:
            audiveris_bin: Audiveris 실행 파일 경로
            
        Raises:
            OmrError: Audiveris 실행 파일을 찾을 수 없을 때
        """
        self.audiveris_bin = Path(audiveris_bin)

        if not self.audiveris_bin.exists():
            raise OmrError(f"Audiveris 실행 파일을 찾을 수 없습니다: {self.audiveris_bin}")

    def image_to_musicxml(self, image_bytes: bytes, suffix: str = ".png") -> str:
        """
        이미지 바이너리를 Audiveris로 돌려 MusicXML 문자열을 반환.
        
        Args:
            image_bytes: 이미지 파일의 바이너리 데이터
            suffix: 이미지 파일 확장자 (기본값: .png)
            
        Returns:
            MusicXML 문자열
            
        Raises:
            OmrError: Audiveris 실행 실패 또는 MusicXML 생성 실패 시
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            img_path = tmpdir / f"input{suffix}"
            out_dir = tmpdir / "out"
            out_dir.mkdir(parents=True, exist_ok=True)

            # 이미지 파일 저장
            img_path.write_bytes(image_bytes)

            # Audiveris 실행 명령
            cmd = [
                str(self.audiveris_bin),
                "-batch",
                "-export",
                "-output", str(out_dir),
                str(img_path),
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(tmpdir),
            )

            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "알 수 없는 오류"
                raise OmrError(f"Audiveris 실행 실패: {error_msg}")

            # MusicXML 파일 찾기
            xml_files = list(out_dir.glob("*.mxl")) + list(out_dir.glob("*.xml"))
            if not xml_files:
                raise OmrError("Audiveris가 MusicXML 파일을 생성하지 못했습니다.")

            # 가장 첫 번째 파일 읽기
            xml_text = xml_files[0].read_text(encoding="utf-8", errors="ignore")
            return xml_text

