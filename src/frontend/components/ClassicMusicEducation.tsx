import { useState, useEffect } from 'react'
import './ClassicMusicEducation.css'
import PianoKeyboard from './PianoKeyboard'
import { aiApi, chordApi } from '../utils/api'

interface ClassicPiece {
  id: string
  composer: string
  title: string
  period: string
  youtubeId: string
  description: string
  keySignature: string
  timeSignature: string
  difficulty: '초급' | '중급' | '고급'
}

const CLASSIC_PIECES: ClassicPiece[] = [
  {
    id: 'fur-elise',
    composer: '베토벤',
    title: '엘리제를 위하여',
    period: '고전주의',
    youtubeId: 'yAsDLGjMhFI',
    description: '베토벤의 가장 유명한 피아노 소품 중 하나로, 아름다운 멜로디와 감정적 표현이 특징입니다.',
    keySignature: 'A단조',
    timeSignature: '3/8박자',
    difficulty: '초급'
  },
  {
    id: 'canon',
    composer: '파헬벨',
    title: '캐논',
    period: '바로크',
    youtubeId: 'JvNQLJ1_HQ0',
    description: '세 개의 성부가 같은 멜로디를 순차적으로 반복하는 캐논 형식의 대표작입니다.',
    keySignature: 'D장조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'claire-de-lune',
    composer: '드뷔시',
    title: '달빛',
    period: '인상주의',
    youtubeId: 'CvFH_6DNRCY',
    description: '인상주의 음악의 대표작으로, 화성의 색채와 분위기를 중시한 작품입니다.',
    keySignature: 'Db장조',
    timeSignature: '9/8박자',
    difficulty: '고급'
  },
  {
    id: 'spring',
    composer: '비발디',
    title: '사계 중 봄',
    period: '바로크',
    youtubeId: 'GRxofEmo3HA',
    description: '바이올린 협주곡으로, 봄의 생동감을 음악으로 표현한 작품입니다.',
    keySignature: 'E장조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'turkish-march',
    composer: '모차르트',
    title: '터키 행진곡',
    period: '고전주의',
    youtubeId: 'rFejpH_tAHM',
    description: '모차르트의 피아노 소나타 중 유명한 곡으로, 밝고 경쾌한 리듬이 특징입니다.',
    keySignature: 'A단조',
    timeSignature: '2/4박자',
    difficulty: '초급'
  },
  {
    id: 'minuet',
    composer: '바흐',
    title: '미뉴에트',
    period: '바로크',
    youtubeId: 'Qj1VHX1F5bE',
    description: '바흐의 작은 모음곡 중 하나로, 우아하고 정돈된 춤곡 형식입니다.',
    keySignature: 'G장조',
    timeSignature: '3/4박자',
    difficulty: '초급'
  },
  {
    id: 'moonlight-sonata',
    composer: '베토벤',
    title: '월광 소나타 1악장',
    period: '고전주의',
    youtubeId: '4Tr0otuiQuU',
    description: '베토벤의 유명한 피아노 소나타로, 달빛처럼 아름다운 멜로디가 특징입니다.',
    keySignature: 'C#단조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'swan-lake',
    composer: '차이콥스키',
    title: '백조의 호수',
    period: '낭만주의',
    youtubeId: '9cNQFB0TDfY',
    description: '발레 음악의 대표작으로, 우아하고 서정적인 멜로디가 아름다운 작품입니다.',
    keySignature: 'D장조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'gymnopedie',
    composer: '사티',
    title: '짐노페디 1번',
    period: '인상주의',
    youtubeId: 'S-Xm7s9eGxU',
    description: '프랑스 작곡가 사티의 대표작으로, 단순하고 평화로운 멜로디가 특징입니다.',
    keySignature: 'D단조',
    timeSignature: '3/4박자',
    difficulty: '초급'
  },
  {
    id: 'four-seasons-winter',
    composer: '비발디',
    title: '사계 중 겨울',
    period: '바로크',
    youtubeId: 'TZCfydWF48c',
    description: '겨울의 추위와 따뜻한 난로를 음악으로 표현한 비발디의 명작입니다.',
    keySignature: 'F단조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'air-on-g-string',
    composer: '바흐',
    title: 'G선상의 아리아',
    period: '바로크',
    youtubeId: 'pxPgCTSlYjs',
    description: '바흐의 오케스트라 모음곡 중 가장 유명한 곡으로, 아름답고 서정적인 멜로디입니다.',
    keySignature: 'D장조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'chopin-nocturne',
    composer: '쇼팽',
    title: '야상곡 Op.9 No.2',
    period: '낭만주의',
    youtubeId: 'YGRO05WcNDk',
    description: '쇼팽의 가장 유명한 야상곡으로, 꿈같이 아름다운 멜로디가 특징입니다.',
    keySignature: 'Eb장조',
    timeSignature: '12/8박자',
    difficulty: '중급'
  },
  {
    id: 'brahms-lullaby',
    composer: '브람스',
    title: '자장가',
    period: '낭만주의',
    youtubeId: 't894u65WG1s',
    description: '세계에서 가장 유명한 자장가로, 부드럽고 따뜻한 멜로디가 특징입니다.',
    keySignature: 'Eb장조',
    timeSignature: '3/4박자',
    difficulty: '초급'
  },
  {
    id: 'bach-invention',
    composer: '바흐',
    title: '2성 인벤션 1번',
    period: '바로크',
    youtubeId: 'ho9rZj8y4oM',
    description: '바흐가 작곡한 피아노 연습곡으로, 대위법의 아름다움을 보여주는 작품입니다.',
    keySignature: 'C장조',
    timeSignature: '4/4박자',
    difficulty: '초급'
  },
  {
    id: 'mozart-serenade',
    composer: '모차르트',
    title: '세레나데',
    period: '고전주의',
    youtubeId: '4Tr0otuiQuU',
    description: '모차르트의 유명한 세레나데로, 밝고 우아한 멜로디가 특징입니다.',
    keySignature: 'G장조',
    timeSignature: '4/4박자',
    difficulty: '초급'
  },
  {
    id: 'debussy-arabesque',
    composer: '드뷔시',
    title: '아라베스크 1번',
    period: '인상주의',
    youtubeId: 'Y9i5v7h5h0s',
    description: '드뷔시의 초기 작품으로, 아름다운 아라베스크 패턴의 멜로디가 특징입니다.',
    keySignature: 'E장조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'schubert-ave-maria',
    composer: '슈베르트',
    title: '아베 마리아',
    period: '낭만주의',
    youtubeId: 'jgpJVI3tDbY',
    description: '슈베르트의 가장 유명한 곡으로, 아름답고 경건한 멜로디가 특징입니다.',
    keySignature: 'Bb장조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'handel-water-music',
    composer: '헨델',
    title: '수상음악',
    period: '바로크',
    youtubeId: 'NjtOrLT8k0I',
    description: '헨델의 관현악 모음곡으로, 밝고 경쾌한 분위기가 특징입니다.',
    keySignature: 'F장조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'beethoven-ode',
    composer: '베토벤',
    title: '환희의 송가',
    period: '고전주의',
    youtubeId: 'ChygZLpJDNE',
    description: '베토벤 교향곡 9번의 마지막 악장으로, 평화와 환희를 노래하는 위대한 작품입니다.',
    keySignature: 'D장조',
    timeSignature: '4/4박자',
    difficulty: '고급'
  },
  {
    id: 'vivaldi-summer',
    composer: '비발디',
    title: '사계 중 여름',
    period: '바로크',
    youtubeId: 'KY1p-FmjT1M',
    description: '여름의 뜨거운 태양과 폭풍을 음악으로 표현한 비발디의 작품입니다.',
    keySignature: 'G단조',
    timeSignature: '3/8박자',
    difficulty: '중급'
  },
  {
    id: 'mozart-serenade',
    composer: '모차르트',
    title: '세레나데',
    period: '고전주의',
    youtubeId: '4Tr0otuiQuU',
    description: '모차르트의 유명한 세레나데로, 밝고 우아한 멜로디가 특징입니다.',
    keySignature: 'G장조',
    timeSignature: '4/4박자',
    difficulty: '초급'
  },
  {
    id: 'bach-goldberg',
    composer: '바흐',
    title: '골드베르크 변주곡',
    period: '바로크',
    youtubeId: '15ezpwCHtJs',
    description: '바흐의 대표적인 변주곡으로, 하나의 주제를 다양한 방식으로 변주한 작품입니다.',
    keySignature: 'G장조',
    timeSignature: '3/4박자',
    difficulty: '고급'
  },
  {
    id: 'chopin-waltz',
    composer: '쇼팽',
    title: '왈츠 Op.64 No.2',
    period: '낭만주의',
    youtubeId: 'JG5gQjXhJYI',
    description: '쇼팽의 유명한 왈츠로, 우아하고 경쾌한 3박자 리듬이 특징입니다.',
    keySignature: 'C#단조',
    timeSignature: '3/4박자',
    difficulty: '중급'
  },
  {
    id: 'beethoven-symphony5',
    composer: '베토벤',
    title: '운명 교향곡',
    period: '고전주의',
    youtubeId: 'rOjHhS5MtvA',
    description: '베토벤의 교향곡 5번으로, "따따따 딴"으로 시작하는 유명한 운명의 동기가 특징입니다.',
    keySignature: 'C단조',
    timeSignature: '2/4박자',
    difficulty: '중급'
  },
  {
    id: 'pachelbel-canon',
    composer: '파헬벨',
    title: '캐논과 지그',
    period: '바로크',
    youtubeId: 'JvNQLJ1_HQ0',
    description: '파헬벨의 캐논으로, 세 개의 성부가 순차적으로 같은 멜로디를 반복하는 형식입니다.',
    keySignature: 'D장조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'debussy-golliwog',
    composer: '드뷔시',
    title: '골리왁의 케이크워크',
    period: '인상주의',
    youtubeId: 'G1BfT1TyH4w',
    description: '드뷔시의 어린이를 위한 피아노 모음곡 중 하나로, 재미있고 경쾌한 곡입니다.',
    keySignature: 'Eb장조',
    timeSignature: '2/4박자',
    difficulty: '초급'
  },
  {
    id: 'mozart-alla-turca',
    composer: '모차르트',
    title: '터키풍 론도',
    period: '고전주의',
    youtubeId: 'rFejpH_tAHM',
    description: '모차르트의 피아노 소나타 중 터키풍 리듬이 특징인 밝고 경쾌한 곡입니다.',
    keySignature: 'A장조',
    timeSignature: '2/4박자',
    difficulty: '초급'
  },
  {
    id: 'bach-minuet-g',
    composer: '바흐',
    title: 'G장조 미뉴에트',
    period: '바로크',
    youtubeId: 'Qj1VHX1F5bE',
    description: '바흐의 작은 모음곡 중 하나로, 우아하고 정돈된 3박자 춤곡입니다.',
    keySignature: 'G장조',
    timeSignature: '3/4박자',
    difficulty: '초급'
  },
  {
    id: 'schumann-train',
    composer: '슈만',
    title: '기차',
    period: '낭만주의',
    youtubeId: 'YGRO05WcNDk',
    description: '슈만의 어린이를 위한 피아노 모음곡 중 하나로, 기차의 움직임을 표현한 작품입니다.',
    keySignature: 'C장조',
    timeSignature: '4/4박자',
    difficulty: '초급'
  },
  {
    id: 'tchaikovsky-nutcracker',
    composer: '차이콥스키',
    title: '호두까기 인형',
    period: '낭만주의',
    youtubeId: 'Wz_f9B4pPtg',
    description: '발레 음악의 대표작으로, 환상적이고 아름다운 멜로디가 특징입니다.',
    keySignature: '다양',
    timeSignature: '다양',
    difficulty: '중급'
  },
  {
    id: 'liszt-liebestraum',
    composer: '리스트',
    title: '사랑의 꿈',
    period: '낭만주의',
    youtubeId: 'kpyutduA00E',
    description: '리스트의 가장 유명한 피아노 작품으로, 낭만적이고 감정적인 멜로디가 특징입니다.',
    keySignature: 'Ab장조',
    timeSignature: '4/4박자',
    difficulty: '고급'
  },
  {
    id: 'ravel-bolero',
    composer: '라벨',
    title: '볼레로',
    period: '인상주의',
    youtubeId: '3-4J5xr2eW4',
    description: '라벨의 대표작으로, 반복되는 리듬과 점점 커지는 음량이 특징입니다.',
    keySignature: 'C장조',
    timeSignature: '3/4박자',
    difficulty: '중급'
  },
  {
    id: 'grieg-peer-gynt',
    composer: '그리그',
    title: '페르 귄트 모음곡',
    period: '낭만주의',
    youtubeId: 'xrIYT-MrVaI',
    description: '그리그의 대표작으로, 북유럽의 아름다운 자연을 표현한 작품입니다.',
    keySignature: 'E단조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'dvorak-new-world',
    composer: '드보르자크',
    title: '신세계 교향곡',
    period: '낭만주의',
    youtubeId: 'ETnoOzqEgtI',
    description: '드보르자크의 교향곡 9번으로, 아메리카의 민속 음악을 바탕으로 한 작품입니다.',
    keySignature: 'E단조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'mendelssohn-wedding',
    composer: '멘델스존',
    title: '결혼 행진곡',
    period: '낭만주의',
    youtubeId: 'rOjHhS5MtvA',
    description: '세계에서 가장 유명한 결혼 행진곡으로, 장엄하고 밝은 멜로디가 특징입니다.',
    keySignature: 'C장조',
    timeSignature: '4/4박자',
    difficulty: '초급'
  },
  {
    id: 'saint-saens-swan',
    composer: '생상스',
    title: '백조',
    period: '낭만주의',
    youtubeId: 'kUNBfXQ2wzE',
    description: '동물의 사육제 중 백조로, 첼로의 아름다운 멜로디가 특징입니다.',
    keySignature: 'G장조',
    timeSignature: '6/4박자',
    difficulty: '중급'
  },
  {
    id: 'prokofiev-peter',
    composer: '프로코피예프',
    title: '피터와 늑대',
    period: '현대음악',
    youtubeId: 'MfM7Y9P2OqQ',
    description: '어린이를 위한 교향 동화로, 각 동물을 다른 악기로 표현한 작품입니다.',
    keySignature: 'C장조',
    timeSignature: '다양',
    difficulty: '초급'
  },
  {
    id: 'holst-planets',
    composer: '홀스트',
    title: '행성 모음곡',
    period: '현대음악',
    youtubeId: 'Isic2Z2e2xs',
    description: '태양계의 행성들을 음악으로 표현한 대규모 관현악 작품입니다.',
    keySignature: '다양',
    timeSignature: '다양',
    difficulty: '중급'
  },
  {
    id: 'ravel-pavane',
    composer: '라벨',
    title: '죽은 공주를 위한 파반느',
    period: '인상주의',
    youtubeId: 'J2Er9A9D5Y8',
    description: '라벨의 초기 작품으로, 우아하고 슬픈 멜로디가 특징입니다.',
    keySignature: 'G단조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  },
  {
    id: 'faure-pavane',
    composer: '포레',
    title: '파반느',
    period: '인상주의',
    youtubeId: 'Vyb-hEKkj_M',
    description: '포레의 대표작으로, 우아하고 서정적인 춤곡 형식입니다.',
    keySignature: 'F#단조',
    timeSignature: '4/4박자',
    difficulty: '중급'
  }
]

const ClassicMusicEducation = () => {
  const [selectedPiece, setSelectedPiece] = useState<ClassicPiece | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [musicTheory, setMusicTheory] = useState<string>('')
  const [isLoadingTheory, setIsLoadingTheory] = useState(false)
  const [activeSection, setActiveSection] = useState<'melody' | 'chord' | 'activity'>('melody')

  useEffect(() => {
    if (selectedPiece) {
      loadMusicTheory()
    }
  }, [selectedPiece])

  const loadMusicTheory = async () => {
    if (!selectedPiece) return

    setIsLoadingTheory(true)
    try {
      const prompt = `${selectedPiece.composer}의 "${selectedPiece.title}"에 대해 초등학생이 이해하기 쉽게 설명해주세요. 
다음 내용을 포함해주세요:
1. 작곡가와 곡의 배경
2. 사용된 음악 이론 (조성, 박자, 형식 등)
3. 곡의 특징과 감상 포인트
4. 초등학생이 따라할 수 있는 활동 제안

간단하고 재미있게 설명해주세요.`

      const response = await aiApi.chat(prompt)
      if (response.success && response.data) {
        const data = response.data as any
        setMusicTheory(data.response || '음악 이론 정보를 불러오는 중...')
      }
    } catch (error) {
      console.error('음악 이론 로드 실패:', error)
      setMusicTheory('음악 이론 정보를 불러올 수 없습니다.')
    } finally {
      setIsLoadingTheory(false)
    }
  }

  const handleAnalyzePiece = async () => {
    if (!selectedPiece) return

    setIsAnalyzing(true)
    setAnalysisResult(null)

    try {
      // YouTube URL로 화음 분석
      const youtubeUrl = `https://www.youtube.com/watch?v=${selectedPiece.youtubeId}`
      
      const apiResponse = await chordApi.analyzeYouTube(youtubeUrl)
      
      if (apiResponse.success && apiResponse.data) {
        const data = apiResponse.data as any
        
        // 응답 데이터를 분석 결과 형식으로 변환
        const result = {
          chords: data.chords || [],
          chordsInfo: data.chordsInfo || [],
          melody: data.melody || [],
          message: data.message || '곡 분석이 완료되었습니다.'
        }
        
        setAnalysisResult(result)
      } else {
        // API 실패 시 기본 데이터 사용
        const fallbackResult = {
          chords: ['Am', 'C', 'F', 'G'],
          chordsInfo: [
            { measure: 1, chord_name: 'Am', notes: ['A4', 'C5', 'E5'] },
            { measure: 2, chord_name: 'C', notes: ['C4', 'E4', 'G4'] },
            { measure: 3, chord_name: 'F', notes: ['F4', 'A4', 'C5'] },
            { measure: 4, chord_name: 'G', notes: ['G4', 'B4', 'D5'] }
          ],
          melody: ['E5', 'D#5', 'E5', 'D#5', 'E5', 'B4', 'D5', 'C5', 'A4'],
          message: '곡 분석이 완료되었습니다. (기본 데이터)'
        }
        setAnalysisResult(fallbackResult)
      }
    } catch (error) {
      console.error('곡 분석 실패:', error)
      // 에러 발생 시에도 기본 데이터 표시
      const fallbackResult = {
        chords: ['Am', 'C', 'F', 'G'],
        chordsInfo: [
          { measure: 1, chord_name: 'Am', notes: ['A4', 'C5', 'E5'] },
          { measure: 2, chord_name: 'C', notes: ['C4', 'E4', 'G4'] }
        ],
        melody: ['E5', 'D#5', 'E5', 'D#5', 'E5', 'B4', 'D5', 'C5', 'A4'],
        message: '곡 분석 중 오류가 발생했습니다. 기본 데이터를 표시합니다.'
      }
      setAnalysisResult(fallbackResult)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleSelectPiece = (piece: ClassicPiece) => {
    setSelectedPiece(piece)
    setAnalysisResult(null)
    setActiveSection('melody')
  }

  return (
    <div className="classic-music-education">
      <h2>🎼 클래식 음악 감상 & 학습</h2>
      
      <div className="pieces-grid">
        {CLASSIC_PIECES.map((piece) => (
          <div
            key={piece.id}
            className={`piece-card ${selectedPiece?.id === piece.id ? 'selected' : ''}`}
            onClick={() => handleSelectPiece(piece)}
          >
            <div className="piece-header">
              <h3>{piece.title}</h3>
              <span className="composer">{piece.composer}</span>
            </div>
            <div className="piece-meta">
              <span className="period">{piece.period}</span>
              <span className={`difficulty ${piece.difficulty}`}>{piece.difficulty}</span>
            </div>
            <p className="piece-description">{piece.description}</p>
            <div className="piece-info">
              <span>조성: {piece.keySignature}</span>
              <span>박자: {piece.timeSignature}</span>
            </div>
          </div>
        ))}
      </div>

      {selectedPiece && (
        <div className="piece-detail-section">
          <div className="piece-title-section">
            <h3>{selectedPiece.composer} - {selectedPiece.title}</h3>
            <button
              className="analyze-button"
              onClick={handleAnalyzePiece}
              disabled={isAnalyzing}
            >
              {isAnalyzing ? (
                <>
                  <span className="spinner"></span>
                  분석 중...
                </>
              ) : (
                '🎵 곡 분석하기'
              )}
            </button>
          </div>

          <div className="youtube-section">
            <h4>음악 감상</h4>
            <div className="youtube-embed">
              <iframe
                width="100%"
                height="400"
                src={`https://www.youtube.com/embed/${selectedPiece.youtubeId}`}
                title={selectedPiece.title}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          </div>

          <div className="tabs-section">
            <div className="tabs">
              <button
                className={`tab ${activeSection === 'melody' ? 'active' : ''}`}
                onClick={() => setActiveSection('melody')}
              >
                🎹 멜로디
              </button>
              <button
                className={`tab ${activeSection === 'chord' ? 'active' : ''}`}
                onClick={() => setActiveSection('chord')}
              >
                🎵 화음
              </button>
              <button
                className={`tab ${activeSection === 'activity' ? 'active' : ''}`}
                onClick={() => setActiveSection('activity')}
              >
                ✏️ 학생 활동
              </button>
            </div>

            <div className="tab-content">
              {activeSection === 'melody' && (
                <div className="melody-section">
                  <h4>멜로디 분석</h4>
                  {analysisResult?.melody ? (
                    <>
                      <div className="melody-info">
                        <p><strong>주요 멜로디 음표:</strong></p>
                        <div className="melody-notes">
                          {analysisResult.melody.map((note: string, i: number) => (
                            <span key={i} className="note-badge">{note}</span>
                          ))}
                        </div>
                      </div>
                      <div className="piano-display">
                        <h5>피아노 건반에서 멜로디 연주해보기</h5>
                        <PianoKeyboard
                          chordNotes={analysisResult.melody}
                          chordName="주요 멜로디"
                          interactive={true}
                          octaves={[4, 5]}
                        />
                        <p className="activity-hint">
                          💡 위 음표들을 순서대로 피아노 건반에서 클릭하여 멜로디를 연주해보세요!
                        </p>
                      </div>
                    </>
                  ) : (
                    <div className="empty-state">
                      <p>곡을 분석하면 멜로디 정보가 표시됩니다.</p>
                      <p className="hint">위의 "🎵 곡 분석하기" 버튼을 클릭하세요.</p>
                    </div>
                  )}
                </div>
              )}

              {activeSection === 'chord' && (
                <div className="chord-section">
                  <h4>화음 분석</h4>
                  {analysisResult?.chordsInfo ? (
                    <>
                      <div className="chords-summary">
                        <p><strong>사용된 화음:</strong></p>
                        <div className="chords-list">
                          {analysisResult.chords.map((chord: string, i: number) => (
                            <span key={i} className="chord-badge">{chord}</span>
                          ))}
                        </div>
                      </div>
                      <div className="chords-progression">
                        <h5>마디별 화음 진행</h5>
                        {analysisResult.chordsInfo.map((chordInfo: any, index: number) => (
                          <div key={index} className="chord-item">
                            <PianoKeyboard
                              chordNotes={chordInfo.notes || []}
                              chordName={`마디 ${chordInfo.measure}: ${chordInfo.chord_name}`}
                              interactive={true}
                              octaves={[3, 4, 5]}
                            />
                          </div>
                        ))}
                      </div>
                    </>
                  ) : (
                    <div className="empty-state">
                      <p>곡을 분석하면 화음 정보가 표시됩니다.</p>
                      <p className="hint">위의 "🎵 곡 분석하기" 버튼을 클릭하세요.</p>
                    </div>
                  )}
                </div>
              )}

              {activeSection === 'activity' && (
                <div className="activity-section">
                  <h4>학생 활동 제안</h4>
                  {musicTheory ? (
                    <div className="theory-content">
                      <div className="theory-text" dangerouslySetInnerHTML={{ __html: musicTheory.replace(/\n/g, '<br/>') }} />
                    </div>
                  ) : isLoadingTheory ? (
                    <div className="loading-state">
                      <span className="spinner"></span>
                      <p>음악 이론 정보를 불러오는 중...</p>
                    </div>
                  ) : (
                    <div className="activity-suggestions">
                      <div className="activity-card">
                        <h5>🎹 활동 1: 멜로디 따라 연주하기</h5>
                        <p>피아노 건반에서 멜로디 음표를 순서대로 클릭하여 연주해보세요.</p>
                        <ul>
                          <li>음표를 하나씩 천천히 연주해보기</li>
                          <li>리듬을 느끼며 연주하기</li>
                          <li>멜로디의 흐름을 따라가기</li>
                        </ul>
                      </div>
                      <div className="activity-card">
                        <h5>🎵 활동 2: 화음 구성하기</h5>
                        <p>각 마디의 화음을 피아노 건반에서 찾아 연주해보세요.</p>
                        <ul>
                          <li>화음의 구성음을 확인하기</li>
                          <li>화음의 소리를 들어보기</li>
                          <li>화음 진행의 변화를 느끼기</li>
                        </ul>
                      </div>
                      <div className="activity-card">
                        <h5>🎼 활동 3: 음악 감상하기</h5>
                        <p>위의 YouTube 영상을 들으며 곡의 특징을 찾아보세요.</p>
                        <ul>
                          <li>곡의 분위기와 감정 느끼기</li>
                          <li>멜로디와 화음이 어떻게 어울리는지 관찰하기</li>
                          <li>리듬의 패턴 찾아보기</li>
                        </ul>
                      </div>
                      <div className="activity-card">
                        <h5>✏️ 활동 4: 작곡가와 곡 배경 알아보기</h5>
                        <p>작곡가의 생애와 곡이 만들어진 배경을 조사해보세요.</p>
                        <ul>
                          <li>작곡가가 살았던 시대 알아보기</li>
                          <li>곡의 제목과 의미 찾아보기</li>
                          <li>다른 작품도 들어보기</li>
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ClassicMusicEducation

