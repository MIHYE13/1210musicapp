"""
PDF Score Parser
Parse PDF music scores and convert to MusicXML
"""

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None
from typing import Optional
from pathlib import Path
import subprocess
import os

class PDFScoreParser:
    """Parse PDF music scores using OMR (Optical Music Recognition)"""
    
    def __init__(self):
        self.temp_dir = Path("temp/pdf")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def parse_pdf_with_audiveris(self, pdf_path: str) -> Optional[str]:
        """
        Parse PDF using Audiveris OMR
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Path to generated MusicXML file
        """
        try:
            output_dir = self.temp_dir / "output"
            output_dir.mkdir(exist_ok=True)
            
            # Run Audiveris CLI
            result = subprocess.run([
                'audiveris',
                '-batch',
                '-export',
                '-output', str(output_dir),
                pdf_path
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # Find generated MusicXML file
                xml_files = list(output_dir.glob("*.mxl")) + list(output_dir.glob("*.xml"))
                if xml_files:
                    return str(xml_files[0])
            
            return None
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None
        except Exception as e:
            st.warning(f"Audiveris 오류: {str(e)}")
            return None
    
    def convert_pdf_to_images(self, pdf_path: str) -> list:
        """
        Convert PDF pages to images for preview
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of image paths
        """
        try:
            from pdf2image import convert_from_path
            
            images = convert_from_path(pdf_path, dpi=200)
            image_paths = []
            
            for i, image in enumerate(images):
                img_path = self.temp_dir / f"page_{i+1}.png"
                image.save(img_path, 'PNG')
                image_paths.append(str(img_path))
            
            return image_paths
            
        except ImportError:
            st.warning("pdf2image 라이브러리가 필요합니다: pip install pdf2image")
            return []
        except Exception as e:
            st.warning(f"PDF 변환 오류: {str(e)}")
            return []
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF (for chord symbols, etc.)
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            import PyPDF2
            
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            return text
            
        except ImportError:
            st.warning("PyPDF2 라이브러리가 필요합니다: pip install PyPDF2")
            return ""
        except Exception as e:
            st.warning(f"텍스트 추출 오류: {str(e)}")
            return ""


def get_pdf_parsing_guide() -> str:
    """Generate guide for PDF music score parsing"""
    
    return """
## 📄 PDF 악보 파싱 가이드

### 현재 지원 상태

PDF 악보를 자동으로 분석하려면 **OMR (Optical Music Recognition)** 기술이 필요합니다.

### 자동 변환 방법

#### 방법 1: Audiveris (권장)

**설치:**
1. Audiveris 다운로드: https://github.com/Audiveris/audiveris/releases
2. Java 필요 (JDK 11+)

**사용:**
```bash
audiveris -batch -export -output output_folder score.pdf
```

#### 방법 2: MuseScore (수동)

1. **MuseScore 설치**
   - https://musescore.org 다운로드
   
2. **PDF 임포트**
   - MuseScore 열기
   - File → Open
   - PDF 파일 선택
   - OMR 실행 (자동)
   
3. **MusicXML 내보내기**
   - File → Export
   - Format: MusicXML
   - 저장

4. **내보낸 파일을 여기에 업로드**

### 방법 3: 온라인 변환기

**SmartScore**
- URL: https://www.musitek.com/smartscore.html
- PDF 업로드
- MusicXML 다운로드

**Dorico** (무료 체험)
- PDF 임포트 지원
- MusicXML 내보내기

### 방법 4: 직접 입력 (가장 정확)

PDF가 복잡하거나 인식이 어려운 경우:

1. **MuseScore에서 직접 입력**
   - 악보 보고 타이핑
   - 가장 정확한 결과
   
2. **MusicXML 저장**
   
3. **여기에 업로드**

---

### 💡 팁

**PDF 품질이 중요합니다!**
- ✅ 깨끗한 스캔 (300 DPI 이상)
- ✅ 흑백 또는 그레이스케일
- ✅ 직선으로 정렬된 악보
- ❌ 손으로 쓴 악보 (인식 어려움)
- ❌ 저화질 이미지
- ❌ 복잡한 레이아웃

**현재 가장 쉬운 방법:**
1. PDF를 MuseScore에서 열기
2. OMR 실행 (자동)
3. 오류 수정
4. MusicXML로 내보내기
5. 여기에 업로드

그러면 화음 분석과 피아노 건반 표시가 자동으로 됩니다! 🎹
"""


def create_pdf_upload_section():
    """Create PDF upload section with guide"""
    
    st.markdown("### 📄 PDF 악보 업로드")
    
    with st.expander("📖 PDF 악보 사용 방법 (클릭)", expanded=False):
        st.markdown(get_pdf_parsing_guide())
    
    pdf_file = st.file_uploader(
        "PDF 악보 파일",
        type=['pdf'],
        help="MuseScore 등으로 MusicXML로 변환 후 업로드를 권장합니다"
    )
    
    if pdf_file:
        # Save PDF
        pdf_path = Path("temp/pdf") / pdf_file.name
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(pdf_path, 'wb') as f:
            f.write(pdf_file.getvalue())
        
        st.success("✅ PDF 파일이 업로드되었습니다!")
        
        # Show preview
        st.info("""
        **다음 단계:**
        
        1. MuseScore나 다른 악보 프로그램에서 이 PDF를 열기
        2. MusicXML 형식으로 내보내기
        3. 오른쪽 '악보 → 처리' 섹션에서 MusicXML 파일 업로드
        
        그러면 자동으로 다장조 변환, 화음 분석, 피아노 건반 표시가 됩니다!
        """)
        
        # Try to extract text (chord symbols)
        parser = PDFScoreParser()
        text = parser.extract_text_from_pdf(str(pdf_path))
        
        if text:
            # Look for chord symbols
            import re
            chords = re.findall(r'\b([A-G][#b]?(?:m|maj|min|dim|aug|sus|7|9)?)\b', text)
            if chords:
                st.write("**발견된 화음 기호:**", ", ".join(set(chords)))
        
        return str(pdf_path)
    
    return None
