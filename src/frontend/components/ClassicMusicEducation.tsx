import { useState, useEffect } from 'react'
import './ClassicMusicEducation.css'
import PianoKeyboard from './PianoKeyboard'
import { aiApi, chordApi, youtubeApi } from '../utils/api'

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

interface YouTubeVideo {
  videoId: string
  title: string
  channel: string
  thumbnail?: string
  url: string
  description?: string
  viewCount?: number
}

const ClassicMusicEducation = () => {
  const [selectedPiece, setSelectedPiece] = useState<ClassicPiece | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  // 음악 이론 관련 상태 (현재 사용하지 않지만 향후 확장 가능)
  // const [musicTheory, setMusicTheory] = useState<string>('')
  // const [isLoadingTheory, setIsLoadingTheory] = useState(false)
  const [activeSection, setActiveSection] = useState<'melody' | 'chord' | 'activity'>('melody')
  
  // 퀴즈 관련 상태
  const [quizMode, setQuizMode] = useState<'none' | 'short-answer' | 'ox'>('none')
  const [quizQuestions, setQuizQuestions] = useState<Array<{
    question: string
    answer: string
    hint?: string
    type: 'short-answer' | 'ox'
    userAnswer?: string
    isCorrect?: boolean
  }>>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState<number>(0)
  const [userAnswer, setUserAnswer] = useState<string>('')
  const [quizScore, setQuizScore] = useState<{ correct: number; total: number }>({ correct: 0, total: 0 })
  const [isLoadingQuiz, setIsLoadingQuiz] = useState(false)
  const [isQuizComplete, setIsQuizComplete] = useState(false)
  const [showHint, setShowHint] = useState<boolean>(false)
  const [showAnswer, setShowAnswer] = useState<boolean>(false)
  
  // 학생 직접 검색 기능
  const [searchMode, setSearchMode] = useState<'classic' | 'search'>('classic')
  const [searchQuery, setSearchQuery] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState<YouTubeVideo[]>([])
  const [selectedVideo, setSelectedVideo] = useState<YouTubeVideo | null>(null)
  const [customYoutubeId, setCustomYoutubeId] = useState<string>('')
  const [noResultsMessage, setNoResultsMessage] = useState<string>('')
  const [aiSuggestion, setAiSuggestion] = useState<string>('')
  const [isLoadingSuggestion, setIsLoadingSuggestion] = useState(false)

  useEffect(() => {
    if (selectedPiece) {
      // 퀴즈 초기화
      setQuizMode('none')
      setQuizQuestions([])
      setCurrentQuestionIndex(0)
      setUserAnswer('')
      setQuizScore({ correct: 0, total: 0 })
      setIsQuizComplete(false)
      setShowHint(false)
      setShowAnswer(false)
    }
  }, [selectedPiece])

  useEffect(() => {
    if (selectedVideo) {
      // 퀴즈 초기화
      setQuizMode('none')
      setQuizQuestions([])
      setCurrentQuestionIndex(0)
      setUserAnswer('')
      setQuizScore({ correct: 0, total: 0 })
      setIsQuizComplete(false)
      setShowHint(false)
      setShowAnswer(false)
    }
  }, [selectedVideo])

  // 문제가 바뀔 때 힌트/정답 표시 상태 초기화
  useEffect(() => {
    setShowHint(false)
    setShowAnswer(false)
  }, [currentQuestionIndex])

  // 퀴즈 문제 생성
  const generateQuiz = async (type: 'short-answer' | 'ox') => {
    if (!selectedPiece && !selectedVideo) return

    setIsLoadingQuiz(true)
    setQuizMode(type)
    setQuizQuestions([])
    setCurrentQuestionIndex(0)
    setUserAnswer('')
    setQuizScore({ correct: 0, total: 0 })
    setIsQuizComplete(false)

    try {
      let prompt = ''
      let pieceInfo: ClassicPiece | null = null
      
      if (selectedPiece) {
        // 추천 곡 감상 모드
        pieceInfo = selectedPiece
        prompt = `${selectedPiece.composer}의 "${selectedPiece.title}"에 대해 초등학생 수준의 음악 퀴즈 문제를 만들어주세요.

요구사항:
- ${type === 'short-answer' ? '단답형 문제 5개' : 'OX형 문제 5개'}
- 초등학생이 이해할 수 있는 쉬운 난이도
- 곡의 특징, 작곡가, 음악 이론 등에 관한 문제
- ${type === 'short-answer' ? '답은 한 단어 또는 짧은 문장으로' : 'O 또는 X로 답할 수 있는 문제'}
- 각 문제마다 힌트를 제공해주세요 (정답을 직접 말하지 않고 도움이 되는 정보)

응답 형식 (JSON):
{
  "questions": [
    {
      "question": "문제 내용",
      "answer": "${type === 'short-answer' ? '정답 (한 단어 또는 짧은 문장)' : 'O 또는 X'}",
      "hint": "힌트 내용 (정답을 직접 말하지 않고 도움이 되는 정보)",
      "type": "${type}"
    }
  ]
}

JSON 형식으로만 응답해주세요.`
      } else if (selectedVideo) {
        // 직접 곡 찾기 모드
        prompt = `다음 YouTube 영상에 대한 초등학생 수준의 음악 퀴즈 문제를 만들어주세요.

영상 정보:
- 제목: "${selectedVideo.title}"
- 채널: "${selectedVideo.channel}"
${selectedVideo.description ? `- 설명: "${selectedVideo.description.substring(0, 200)}"` : ''}

요구사항:
- ${type === 'short-answer' ? '단답형 문제 5개' : 'OX형 문제 5개'}
- 초등학생이 이해할 수 있는 쉬운 난이도
- 영상의 내용, 음악 특징, 악기, 리듬 등에 관한 문제
- ${type === 'short-answer' ? '답은 한 단어 또는 짧은 문장으로' : 'O 또는 X로 답할 수 있는 문제'}
- 각 문제마다 힌트를 제공해주세요 (정답을 직접 말하지 않고 도움이 되는 정보)

응답 형식 (JSON):
{
  "questions": [
    {
      "question": "문제 내용",
      "answer": "${type === 'short-answer' ? '정답 (한 단어 또는 짧은 문장)' : 'O 또는 X'}",
      "hint": "힌트 내용 (정답을 직접 말하지 않고 도움이 되는 정보)",
      "type": "${type}"
    }
  ]
}

JSON 형식으로만 응답해주세요.`
      }

      const response = await aiApi.chat(prompt)
      if (response.success && response.data) {
        const data = response.data as any
        let questions: Array<{ question: string; answer: string; type: 'short-answer' | 'ox' }> = []
        
        // JSON 파싱 시도
        try {
          const responseText = data.response || data.message || JSON.stringify(data)
          // JSON 부분 추출
          const jsonMatch = responseText.match(/\{[\s\S]*\}/)
          if (jsonMatch) {
            const parsed = JSON.parse(jsonMatch[0])
            questions = (parsed.questions || []).map((q: any) => ({
              ...q,
              hint: q.hint || (pieceInfo ? generateDefaultHint(q.question, q.answer, pieceInfo) : '영상을 다시 한번 확인해보세요.')
            }))
          } else {
            // JSON이 아닌 경우 기본 문제 생성
            questions = generateDefaultQuestions(type)
          }
        } catch (e) {
          // 파싱 실패 시 기본 문제 생성
          questions = generateDefaultQuestions(type)
        }

        if (questions.length === 0) {
          questions = generateDefaultQuestions(type)
        }

        setQuizQuestions(questions)
        setQuizScore({ correct: 0, total: questions.length })
      } else {
        // 기본 문제 생성
        const defaultQuestions = generateDefaultQuestions(type)
        setQuizQuestions(defaultQuestions)
        setQuizScore({ correct: 0, total: defaultQuestions.length })
      }
    } catch (error) {
      console.error('퀴즈 생성 실패:', error)
      // 기본 문제 생성
      const defaultQuestions = generateDefaultQuestions(type)
      setQuizQuestions(defaultQuestions)
      setQuizScore({ correct: 0, total: defaultQuestions.length })
    } finally {
      setIsLoadingQuiz(false)
    }
  }

  // 기본 힌트 생성
  const generateDefaultHint = (question: string, answer: string, piece: ClassicPiece): string => {
    if (question.includes('작곡가')) {
      return `이 작곡가는 ${piece.period} 시대의 유명한 작곡가입니다.`
    } else if (question.includes('시대')) {
      return `이 곡은 ${piece.period} 시대에 작곡되었습니다.`
    } else if (question.includes('조성')) {
      return `곡의 조성은 ${piece.keySignature}입니다.`
    } else if (question.includes('박자')) {
      return `곡의 박자는 ${piece.timeSignature}입니다.`
    } else if (question.includes('난이도')) {
      return `이 곡의 난이도는 ${piece.difficulty}입니다.`
    } else {
      return `곡의 정보를 다시 한번 확인해보세요.`
    }
  }

  // 기본 문제 생성 (AI 실패 시 사용)
  const generateDefaultQuestions = (type: 'short-answer' | 'ox'): Array<{ question: string; answer: string; hint?: string; type: 'short-answer' | 'ox' }> => {
    if (selectedPiece) {
      // 추천 곡 감상 모드
      if (type === 'short-answer') {
        return [
          {
            question: `${selectedPiece.composer}의 "${selectedPiece.title}"의 작곡가는 누구인가요?`,
            answer: selectedPiece.composer,
            hint: `이 작곡가는 ${selectedPiece.period} 시대의 유명한 작곡가입니다.`,
            type: 'short-answer'
          },
          {
            question: `이 곡의 시대는 무엇인가요?`,
            answer: selectedPiece.period,
            hint: `이 곡은 ${selectedPiece.period} 시대에 작곡되었습니다.`,
            type: 'short-answer'
          },
          {
            question: `이 곡의 조성은 무엇인가요?`,
            answer: selectedPiece.keySignature.replace('장조', '').replace('단조', ''),
            hint: `곡의 조성은 ${selectedPiece.keySignature}입니다.`,
            type: 'short-answer'
          },
          {
            question: `이 곡의 박자는 무엇인가요?`,
            answer: selectedPiece.timeSignature,
            hint: `곡의 박자는 ${selectedPiece.timeSignature}입니다.`,
            type: 'short-answer'
          },
          {
            question: `이 곡의 난이도는 무엇인가요?`,
            answer: selectedPiece.difficulty,
            hint: `이 곡의 난이도는 ${selectedPiece.difficulty}입니다.`,
            type: 'short-answer'
          }
        ]
      } else {
        return [
          {
            question: `${selectedPiece.composer}는 고전주의 시대의 작곡가입니다.`,
            answer: selectedPiece.period === '고전주의' ? 'O' : 'X',
            hint: `${selectedPiece.composer}는 ${selectedPiece.period} 시대의 작곡가입니다.`,
            type: 'ox'
          },
          {
            question: `이 곡의 조성은 ${selectedPiece.keySignature}입니다.`,
            answer: 'O',
            hint: `곡의 조성 정보를 확인해보세요.`,
            type: 'ox'
          },
          {
            question: `이 곡은 ${selectedPiece.timeSignature}박자로 되어 있습니다.`,
            answer: 'O',
            hint: `곡의 박자 정보를 확인해보세요.`,
            type: 'ox'
          },
          {
            question: `이 곡은 매우 어려운 곡입니다.`,
            answer: selectedPiece.difficulty === '고급' ? 'O' : 'X',
            hint: `이 곡의 난이도는 ${selectedPiece.difficulty}입니다.`,
            type: 'ox'
          },
          {
            question: `${selectedPiece.composer}는 바로크 시대의 작곡가입니다.`,
            answer: selectedPiece.period === '바로크' ? 'O' : 'X',
            hint: `${selectedPiece.composer}는 ${selectedPiece.period} 시대의 작곡가입니다.`,
            type: 'ox'
          }
        ]
      }
    } else if (selectedVideo) {
      // 직접 곡 찾기 모드 - 영상 제목 기반 기본 문제
      const videoTitle = selectedVideo.title
      if (type === 'short-answer') {
        return [
          {
            question: `이 영상의 제목은 무엇인가요?`,
            answer: videoTitle,
            hint: `영상 제목을 다시 한번 확인해보세요.`,
            type: 'short-answer'
          },
          {
            question: `이 영상의 채널 이름은 무엇인가요?`,
            answer: selectedVideo.channel,
            hint: `영상 정보를 확인해보세요.`,
            type: 'short-answer'
          },
          {
            question: `이 영상에서 들리는 음악의 특징을 한 단어로 표현하면?`,
            answer: '음악',
            hint: `영상을 다시 들어보고 음악의 특징을 생각해보세요.`,
            type: 'short-answer'
          },
          {
            question: `이 영상에서 사용된 악기는 무엇인가요?`,
            answer: '피아노',
            hint: `영상을 시청하면서 어떤 악기가 나오는지 확인해보세요.`,
            type: 'short-answer'
          },
          {
            question: `이 음악의 느낌을 한 단어로 표현하면?`,
            answer: '아름다운',
            hint: `음악을 듣고 어떤 느낌인지 생각해보세요.`,
            type: 'short-answer'
          }
        ]
      } else {
        return [
          {
            question: `이 영상은 음악 교육 영상입니다.`,
            answer: 'O',
            hint: `영상의 내용을 확인해보세요.`,
            type: 'ox'
          },
          {
            question: `이 영상에서 피아노 소리가 들립니다.`,
            answer: 'O',
            hint: `영상을 들어보면서 어떤 악기 소리가 나는지 확인해보세요.`,
            type: 'ox'
          },
          {
            question: `이 음악은 빠른 템포입니다.`,
            answer: 'X',
            hint: `음악의 속도를 다시 들어보세요.`,
            type: 'ox'
          },
          {
            question: `이 영상은 클래식 음악에 관한 내용입니다.`,
            answer: 'O',
            hint: `영상의 내용을 확인해보세요.`,
            type: 'ox'
          },
          {
            question: `이 음악은 조용한 느낌입니다.`,
            answer: 'O',
            hint: `음악의 분위기를 다시 들어보세요.`,
            type: 'ox'
          }
        ]
      }
    }
    
    return []
  }

  // 답안 제출
  const handleSubmitAnswer = () => {
    if (!userAnswer.trim() || 
        currentQuestionIndex >= quizQuestions.length || 
        quizQuestions.length === 0 ||
        quizMode === 'none') return

    const currentQuestion = quizQuestions[currentQuestionIndex]
    if (!currentQuestion) return

    let isCorrect = false

    if (quizMode === 'ox') {
      isCorrect = userAnswer.trim().toUpperCase() === currentQuestion.answer.toUpperCase()
    } else if (quizMode === 'short-answer') {
      // 단답형: 대소문자 무시하고 비교
      const normalizedUserAnswer = userAnswer.trim().toLowerCase()
      const normalizedCorrectAnswer = currentQuestion.answer.toLowerCase()
      isCorrect = normalizedUserAnswer === normalizedCorrectAnswer || 
                  normalizedCorrectAnswer.includes(normalizedUserAnswer) ||
                  normalizedUserAnswer.includes(normalizedCorrectAnswer)
    }

    // 문제 업데이트
    const updatedQuestions = [...quizQuestions]
    updatedQuestions[currentQuestionIndex] = {
      ...currentQuestion,
      userAnswer: userAnswer.trim(),
      isCorrect
    }
    setQuizQuestions(updatedQuestions)

    // 점수 업데이트
    if (isCorrect) {
      setQuizScore(prev => ({ ...prev, correct: prev.correct + 1 }))
    }

    // 다음 문제로 이동 또는 완료
    if (currentQuestionIndex < quizQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setUserAnswer('')
    } else {
      setIsQuizComplete(true)
    }
  }

  // 퀴즈 다시 시작
  const handleRestartQuiz = () => {
    if (quizQuestions.length === 0) return
    setCurrentQuestionIndex(0)
    setUserAnswer('')
    setQuizScore({ correct: 0, total: quizQuestions.length })
    setIsQuizComplete(false)
    setShowHint(false)
    setShowAnswer(false)
    // 사용자 답안 초기화
    const resetQuestions = quizQuestions.map(q => ({
      ...q,
      userAnswer: undefined,
      isCorrect: undefined
    }))
    setQuizQuestions(resetQuestions)
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
    setSelectedVideo(null)
    setCustomYoutubeId('')
  }

  // 작곡가의 다른 곡 제안 요청
  const requestComposerSuggestions = async (query: string) => {
    setIsLoadingSuggestion(true)
    setAiSuggestion('')
    
    try {
      const prompt = `다음 검색어에서 작곡가나 음악가 이름을 추출하고, 해당 작곡가(음악가)의 다른 유명한 곡들을 초등학생이 이해하기 쉽게 3-5개 추천해주세요.

검색어: "${query}"

요구사항:
- 작곡가/음악가 이름을 먼저 언급
- 각 곡의 제목과 간단한 특징 설명
- 초등학생이 이해할 수 있는 쉬운 언어 사용
- 한국어로 응답

응답 형식:
작곡가 이름: [작곡가 이름]

추천 곡:
1. [곡 제목] - [간단한 설명]
2. [곡 제목] - [간단한 설명]
...`

      const response = await aiApi.chat(prompt)
      if (response.success && response.data) {
        const data = response.data as any
        const suggestionText = data.response || data.message || JSON.stringify(data)
        setAiSuggestion(suggestionText)
      } else {
        setAiSuggestion('죄송합니다. 추천 곡을 불러올 수 없습니다.')
      }
    } catch (error) {
      console.error('작곡가 추천 실패:', error)
      setAiSuggestion('죄송합니다. 추천 곡을 불러올 수 없습니다.')
    } finally {
      setIsLoadingSuggestion(false)
    }
  }

  // YouTube 검색
  const handleSearchYouTube = async () => {
    if (!searchQuery.trim()) {
      alert('검색어를 입력해주세요.')
      return
    }

    setIsSearching(true)
    setSearchResults([])
    setError(null)
    setNoResultsMessage('')
    setAiSuggestion('')

    try {
      const response = await youtubeApi.search(searchQuery, 10)
      console.log('YouTube 검색 응답:', response)
      
      if (response.success && response.data) {
        const data = response.data as any
        const videos: YouTubeVideo[] = (data.videos || []).map((v: any) => ({
          videoId: v.videoId || v.id || v.video_id,
          title: v.title,
          channel: v.channel || v.channelTitle || v.channel_title || '',
          thumbnail: v.thumbnail,
          url: `https://www.youtube.com/watch?v=${v.videoId || v.id || v.video_id}`,
          description: v.description || '',
          viewCount: v.viewCount || v.view_count
        }))
        
        if (videos.length === 0) {
          // 검색 결과가 없을 때
          setNoResultsMessage(`"${searchQuery}"에 대한 검색 결과가 없습니다.`)
          // AI를 통해 작곡가의 다른 곡 제안
          await requestComposerSuggestions(searchQuery)
        } else {
          setSearchResults(videos)
        }
      } else {
        // API 응답 실패
        const errorMsg = response.error || '검색 결과를 불러올 수 없습니다.'
        setError(errorMsg)
        setNoResultsMessage(`"${searchQuery}"에 대한 검색 결과를 불러올 수 없습니다.`)
        // AI를 통해 작곡가의 다른 곡 제안
        await requestComposerSuggestions(searchQuery)
      }
    } catch (error) {
      console.error('YouTube 검색 실패:', error)
      const errorMsg = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      setError(errorMsg)
      setNoResultsMessage(`"${searchQuery}"에 대한 검색 중 오류가 발생했습니다.`)
      // AI를 통해 작곡가의 다른 곡 제안
      await requestComposerSuggestions(searchQuery)
    } finally {
      setIsSearching(false)
    }
  }

  // YouTube URL에서 ID 추출
  const extractVideoId = (url: string): string | null => {
    const patterns = [
      /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/,
      /^([a-zA-Z0-9_-]{11})$/,
    ]
    for (const pattern of patterns) {
      const match = url.match(pattern)
      if (match) return match[1]
    }
    return null
  }

  // 직접 URL 입력으로 분석
  const handleAnalyzeCustomVideo = async (video: YouTubeVideo | string) => {
    let videoId: string
    let videoUrl: string

    if (typeof video === 'string') {
      // URL 문자열인 경우
      const extractedId = extractVideoId(video)
      if (!extractedId) {
        alert('올바른 YouTube URL을 입력해주세요.')
        return
      }
      videoId = extractedId
      videoUrl = video.startsWith('http') ? video : `https://www.youtube.com/watch?v=${extractedId}`
    } else {
      // YouTubeVideo 객체인 경우
      videoId = video.videoId
      videoUrl = video.url
      setSelectedVideo(video)
      setCustomYoutubeId(videoId)
    }

    setIsAnalyzing(true)
    setAnalysisResult(null)

    try {
      const apiResponse = await chordApi.analyzeYouTube(videoUrl)
      
      if (apiResponse.success && apiResponse.data) {
        const data = apiResponse.data as any
        const result = {
          chords: data.chords || [],
          chordsInfo: data.chordsInfo || [],
          melody: data.melody || [],
          message: data.message || '곡 분석이 완료되었습니다.'
        }
        setAnalysisResult(result)
        setActiveSection('melody')
      } else {
        // 기본 데이터 사용
        const fallbackResult = {
          chords: ['Am', 'C', 'F', 'G'],
          chordsInfo: [
            { measure: 1, chord_name: 'Am', notes: ['A4', 'C5', 'E5'] },
            { measure: 2, chord_name: 'C', notes: ['C4', 'E4', 'G4'] }
          ],
          melody: ['E5', 'D#5', 'E5', 'D#5', 'E5', 'B4', 'D5', 'C5', 'A4'],
          message: '곡 분석이 완료되었습니다. (기본 데이터)'
        }
        setAnalysisResult(fallbackResult)
        setActiveSection('melody')
      }
    } catch (error) {
      console.error('곡 분석 실패:', error)
      alert('곡 분석 중 오류가 발생했습니다.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const [error, setError] = useState<string | null>(null)

  // 현재 표시할 YouTube ID 결정
  const getCurrentYoutubeId = (): string => {
    if (customYoutubeId) return customYoutubeId
    if (selectedPiece) return selectedPiece.youtubeId
    return ''
  }

  return (
    <div className="classic-music-education">
      <h2>🎼 클래식 음악 감상 & 학습</h2>
      
      {/* 모드 선택 */}
      <div className="mode-selector">
        <button
          className={`mode-button ${searchMode === 'classic' ? 'active' : ''}`}
          onClick={() => {
            setSearchMode('classic')
            setSelectedVideo(null)
            setCustomYoutubeId('')
            setAnalysisResult(null)
          }}
        >
          📚 추천 곡 감상
        </button>
        <button
          className={`mode-button ${searchMode === 'search' ? 'active' : ''}`}
          onClick={() => {
            setSearchMode('search')
            setSelectedPiece(null)
            setAnalysisResult(null)
          }}
        >
          🔍 직접 곡 찾기
        </button>
      </div>

      {searchMode === 'classic' && (
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
      )}

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
                src={`https://www.youtube.com/embed/${getCurrentYoutubeId()}?rel=0`}
                title={selectedPiece?.title || selectedVideo?.title || '음악 감상'}
                frameBorder="0"
                allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                style={{ border: 'none', borderRadius: '8px' }}
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
                  <h4>🎯 음악 퀴즈</h4>
                  
                  {!selectedPiece ? (
                    <div className="quiz-mode-selection">
                      <p className="quiz-intro">
                        먼저 위에서 곡을 선택해주세요!
                      </p>
                      <p className="quiz-hint">
                        곡을 선택하면 해당 곡에 대한 퀴즈를 풀 수 있습니다.
                      </p>
                    </div>
                  ) : quizMode === 'none' ? (
                    <div className="quiz-mode-selection">
                      <p className="quiz-intro">
                        {selectedPiece.composer}의 "{selectedPiece.title}"에 대한 퀴즈를 풀어보세요!
                      </p>
                      <div className="quiz-mode-buttons">
                        <button
                          className="quiz-mode-button"
                          onClick={() => generateQuiz('short-answer')}
                          disabled={isLoadingQuiz || !selectedPiece}
                        >
                          📝 단답형 퀴즈
                          <span className="quiz-mode-desc">5문제</span>
                        </button>
                        <button
                          className="quiz-mode-button"
                          onClick={() => generateQuiz('ox')}
                          disabled={isLoadingQuiz || !selectedPiece}
                        >
                          ✅ OX형 퀴즈
                          <span className="quiz-mode-desc">5문제</span>
                        </button>
                      </div>
                      {isLoadingQuiz && (
                        <div className="loading-state">
                          <span className="spinner"></span>
                          <p>퀴즈 문제를 생성하는 중...</p>
                        </div>
                      )}
                    </div>
                  ) : isQuizComplete ? (
                    <div className="quiz-result">
                      <div className="quiz-score-display">
                        <h3>퀴즈 완료! 🎉</h3>
                        <div className="score-circle">
                          <div className="score-number">{quizScore.correct}</div>
                          <div className="score-total">/ {quizScore.total}</div>
                        </div>
                        <div className="score-percentage">
                          {Math.round((quizScore.correct / quizScore.total) * 100)}점
                        </div>
                      </div>
                      
                      <div className="quiz-review">
                        <h4>문제 리뷰</h4>
                        {quizQuestions.map((q, index) => (
                          <div key={index} className={`quiz-review-item ${q.isCorrect ? 'correct' : 'incorrect'}`}>
                            <div className="review-question">
                              <span className="question-number">Q{index + 1}.</span>
                              {q.question}
                            </div>
                            <div className="review-answer">
                              <div className="answer-section">
                                <span className="answer-label">정답:</span>
                                <span className="correct-answer">{q.answer}</span>
                              </div>
                              {q.userAnswer && (
                                <div className="answer-section">
                                  <span className="answer-label">내 답:</span>
                                  <span className={`user-answer ${q.isCorrect ? 'correct' : 'incorrect'}`}>
                                    {q.userAnswer}
                                  </span>
                                </div>
                              )}
                              <span className={`result-badge ${q.isCorrect ? 'correct' : 'incorrect'}`}>
                                {q.isCorrect ? '✓ 정답!' : '✗ 오답'}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                      
                      <div className="quiz-actions">
                        <button className="restart-button" onClick={handleRestartQuiz}>
                          🔄 다시 풀기
                        </button>
                        <button className="new-quiz-button" onClick={() => {
                          setQuizMode('none')
                          setQuizQuestions([])
                          setCurrentQuestionIndex(0)
                          setUserAnswer('')
                          setQuizScore({ correct: 0, total: 0 })
                          setIsQuizComplete(false)
                        }}>
                          📝 다른 퀴즈 풀기
                        </button>
                      </div>
                    </div>
                  ) : quizQuestions.length > 0 ? (
                    <div className="quiz-container">
                      <div className="quiz-progress">
                        <div className="progress-bar">
                          <div 
                            className="progress-fill" 
                            style={{ width: `${Math.min(((currentQuestionIndex + 1) / quizQuestions.length) * 100, 100)}%` }}
                          />
                        </div>
                        <span className="progress-text">
                          {Math.min(currentQuestionIndex + 1, quizQuestions.length)} / {quizQuestions.length}
                        </span>
                      </div>
                      
                      <div className="quiz-question-card">
                        <div className="question-header">
                          <span className="question-type-badge">
                            {quizMode === 'ox' ? 'OX형' : '단답형'}
                          </span>
                          <span className="question-number-large">Q{Math.min(currentQuestionIndex + 1, quizQuestions.length)}</span>
                        </div>
                        <div className="question-text">
                          {quizQuestions[currentQuestionIndex]?.question || '문제를 불러오는 중...'}
                        </div>
                        
                        {/* 힌트 표시 */}
                        {showHint && quizQuestions[currentQuestionIndex]?.hint && (
                          <div className="quiz-hint-box">
                            <div className="hint-icon">💡</div>
                            <div className="hint-text">{quizQuestions[currentQuestionIndex].hint}</div>
                          </div>
                        )}
                        
                        {/* 정답 표시 */}
                        {showAnswer && (
                          <div className="quiz-answer-box">
                            <div className="answer-icon">✓</div>
                            <div className="answer-text">
                              <span className="answer-label-text">정답: </span>
                              <span className="answer-value">{quizQuestions[currentQuestionIndex]?.answer}</span>
                            </div>
                          </div>
                        )}
                        
                        {/* 힌트/정답 버튼 */}
                        <div className="quiz-help-buttons">
                          {quizQuestions[currentQuestionIndex]?.hint && (
                            <button
                              className="hint-button"
                              onClick={() => setShowHint(!showHint)}
                            >
                              {showHint ? '💡 힌트 숨기기' : '💡 힌트 보기'}
                            </button>
                          )}
                          <button
                            className="answer-button"
                            onClick={() => {
                              const newShowAnswer = !showAnswer
                              setShowAnswer(newShowAnswer)
                              // 정답 확인 시 자동으로 답안 입력란에 정답 채우기
                              if (newShowAnswer && quizQuestions[currentQuestionIndex]) {
                                const currentAnswer = quizQuestions[currentQuestionIndex].answer
                                if (quizMode === 'ox') {
                                  setUserAnswer(currentAnswer.toUpperCase())
                                } else {
                                  setUserAnswer(currentAnswer)
                                }
                              }
                            }}
                          >
                            {showAnswer ? '✓ 정답 숨기기' : '✓ 정답 확인'}
                          </button>
                        </div>
                        
                        {quizMode === 'ox' ? (
                          <div className="ox-answers">
                            <button
                              className={`ox-button ${userAnswer === 'O' ? 'selected' : ''}`}
                              onClick={() => setUserAnswer('O')}
                            >
                              O (맞음)
                            </button>
                            <button
                              className={`ox-button ${userAnswer === 'X' ? 'selected' : ''}`}
                              onClick={() => setUserAnswer('X')}
                            >
                              X (틀림)
                            </button>
                          </div>
                        ) : (
                          <div className="short-answer-input">
                            <input
                              type="text"
                              className="answer-input"
                              placeholder="답을 입력하세요"
                              value={userAnswer}
                              onChange={(e) => setUserAnswer(e.target.value)}
                              onKeyPress={(e) => {
                                if (e.key === 'Enter') {
                                  handleSubmitAnswer()
                                }
                              }}
                            />
                          </div>
                        )}
                        
                        <button
                          className="submit-answer-button"
                          onClick={handleSubmitAnswer}
                          disabled={!userAnswer.trim()}
                        >
                          {currentQuestionIndex < quizQuestions.length - 1 ? '다음 문제 →' : '제출하기 ✓'}
                        </button>
                      </div>
                      
                      <div className="quiz-score-mini">
                        현재 점수: {quizScore.correct} / {currentQuestionIndex} {currentQuestionIndex > 0 && quizScore.correct > 0 ? `(${Math.round((quizScore.correct / currentQuestionIndex) * 100)}%)` : ''}
                      </div>
                    </div>
                  ) : (
                    <div className="loading-state">
                      <span className="spinner"></span>
                      <p>퀴즈 문제를 생성하는 중...</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {searchMode === 'search' && (
        <div className="search-section">
          <div className="search-controls">
            <div className="search-input-group">
              <input
                type="text"
                className="search-input"
                placeholder="곡 제목, 작곡가 이름 등을 검색하세요 (예: 베토벤 운명)"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    handleSearchYouTube()
                  }
                }}
              />
              <button
                className="search-button"
                onClick={handleSearchYouTube}
                disabled={isSearching}
              >
                {isSearching ? '검색 중...' : '🔍 검색'}
              </button>
            </div>
            
            <div className="url-input-group">
              <input
                type="text"
                className="url-input"
                placeholder="또는 YouTube URL을 직접 입력하세요"
                onChange={(e) => {
                  const url = e.target.value
                  const videoId = extractVideoId(url)
                  if (videoId) {
                    setCustomYoutubeId(videoId)
                  }
                }}
              />
              <button
                className="analyze-button"
                onClick={() => {
                  if (customYoutubeId) {
                    handleAnalyzeCustomVideo(`https://www.youtube.com/watch?v=${customYoutubeId}`)
                  } else {
                    alert('YouTube URL을 입력해주세요.')
                  }
                }}
                disabled={!customYoutubeId || isAnalyzing}
              >
                {isAnalyzing ? '분석 중...' : '🎵 분석하기'}
              </button>
            </div>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {noResultsMessage && (
            <div className="no-results-section">
              <div className="no-results-message">
                <div className="no-results-icon">🔍</div>
                <h3>{noResultsMessage}</h3>
                <p>다른 검색어로 시도해보시거나, 아래 추천 곡을 확인해보세요!</p>
              </div>
              
              {isLoadingSuggestion ? (
                <div className="suggestion-loading">
                  <span className="spinner"></span>
                  <p>추천 곡을 찾는 중...</p>
                </div>
              ) : aiSuggestion && (
                <div className="ai-suggestion-box">
                  <div className="suggestion-header">
                    <div className="suggestion-icon">💡</div>
                    <h4>추천 곡</h4>
                  </div>
                  <div className="suggestion-content">
                    <pre className="suggestion-text">{aiSuggestion}</pre>
                  </div>
                </div>
              )}
            </div>
          )}

          {searchResults.length > 0 && (
            <div className="search-results">
              <h3>검색 결과</h3>
              <div className="videos-grid">
                {searchResults.map((video) => (
                  <div
                    key={video.videoId}
                    className={`video-card ${selectedVideo?.videoId === video.videoId ? 'selected' : ''}`}
                    onClick={() => {
                      setSelectedVideo(video)
                      setCustomYoutubeId(video.videoId)
                    }}
                  >
                    {video.thumbnail && (
                      <div className="video-thumbnail">
                        <img src={video.thumbnail} alt={video.title} />
                        <div className="play-overlay">▶</div>
                      </div>
                    )}
                    <div className="video-info">
                      <h4>{video.title}</h4>
                      <p className="video-channel">{video.channel}</p>
                      {video.viewCount && (
                        <p className="video-views">
                          조회수: {video.viewCount.toLocaleString()}회
                        </p>
                      )}
                    </div>
                    <button
                      className="analyze-video-button"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleAnalyzeCustomVideo(video)
                      }}
                      disabled={isAnalyzing}
                    >
                      {isAnalyzing ? '분석 중...' : '🎵 분석하기'}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {selectedVideo && (
            <div className="selected-video-section">
              <h3>선택된 영상</h3>
              <div className="youtube-section">
                <div className="youtube-embed">
                  <iframe
                    width="100%"
                    height="400"
                    src={`https://www.youtube.com/embed/${selectedVideo.videoId}?rel=0`}
                    title={selectedVideo.title}
                    frameBorder="0"
                    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                    style={{ border: 'none', borderRadius: '8px' }}
                  />
                </div>
              </div>
            </div>
          )}

          {analysisResult && (
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
                    {analysisResult.melody ? (
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
                        </div>
                      </>
                    ) : (
                      <div className="empty-state">
                        <p>멜로디 정보를 불러올 수 없습니다.</p>
                      </div>
                    )}
                  </div>
                )}

                {activeSection === 'chord' && (
                  <div className="chord-section">
                    <h4>화음 분석</h4>
                    {analysisResult.chordsInfo ? (
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
                        <p>화음 정보를 불러올 수 없습니다.</p>
                      </div>
                    )}
                  </div>
                )}

                {activeSection === 'activity' && (
                  <div className="activity-section">
                    <h4>🎯 음악 퀴즈</h4>
                    
                    {!selectedVideo ? (
                      <div className="quiz-mode-selection">
                        <p className="quiz-intro">
                          먼저 위에서 영상을 선택해주세요!
                        </p>
                        <p className="quiz-hint">
                          영상을 선택하면 해당 영상에 대한 퀴즈를 풀 수 있습니다.
                        </p>
                      </div>
                    ) : quizMode === 'none' ? (
                      <div className="quiz-mode-selection">
                        <p className="quiz-intro">
                          "{selectedVideo.title}"에 대한 퀴즈를 풀어보세요!
                        </p>
                        <div className="quiz-mode-buttons">
                          <button
                            className="quiz-mode-button"
                            onClick={() => generateQuiz('short-answer')}
                            disabled={isLoadingQuiz || !selectedVideo}
                          >
                            📝 단답형 퀴즈
                            <span className="quiz-mode-desc">5문제</span>
                          </button>
                          <button
                            className="quiz-mode-button"
                            onClick={() => generateQuiz('ox')}
                            disabled={isLoadingQuiz || !selectedVideo}
                          >
                            ✅ OX형 퀴즈
                            <span className="quiz-mode-desc">5문제</span>
                          </button>
                        </div>
                        {isLoadingQuiz && (
                          <div className="loading-state">
                            <span className="spinner"></span>
                            <p>퀴즈 문제를 생성하는 중...</p>
                          </div>
                        )}
                      </div>
                    ) : isQuizComplete ? (
                      <div className="quiz-result">
                        <div className="quiz-score-display">
                          <h3>퀴즈 완료! 🎉</h3>
                          <div className="score-circle">
                            <div className="score-number">{quizScore.correct}</div>
                            <div className="score-total">/ {quizScore.total}</div>
                          </div>
                          <div className="score-percentage">
                            {Math.round((quizScore.correct / quizScore.total) * 100)}점
                          </div>
                        </div>
                        
                        <div className="quiz-review">
                          <h4>문제 리뷰</h4>
                          {quizQuestions.map((q, index) => (
                            <div key={index} className={`quiz-review-item ${q.isCorrect ? 'correct' : 'incorrect'}`}>
                              <div className="review-question">
                                <span className="question-number">Q{index + 1}.</span>
                                {q.question}
                              </div>
                              <div className="review-answer">
                                <div className="answer-section">
                                  <span className="answer-label">정답:</span>
                                  <span className="correct-answer">{q.answer}</span>
                                </div>
                                {q.userAnswer && (
                                  <div className="answer-section">
                                    <span className="answer-label">내 답:</span>
                                    <span className={`user-answer ${q.isCorrect ? 'correct' : 'incorrect'}`}>
                                      {q.userAnswer}
                                    </span>
                                  </div>
                                )}
                                <span className={`result-badge ${q.isCorrect ? 'correct' : 'incorrect'}`}>
                                  {q.isCorrect ? '✓ 정답!' : '✗ 오답'}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                        
                        <div className="quiz-actions">
                          <button className="restart-button" onClick={handleRestartQuiz}>
                            🔄 다시 풀기
                          </button>
                          <button className="new-quiz-button" onClick={() => {
                            setQuizMode('none')
                            setQuizQuestions([])
                            setCurrentQuestionIndex(0)
                            setUserAnswer('')
                            setQuizScore({ correct: 0, total: 0 })
                            setIsQuizComplete(false)
                          }}>
                            📝 다른 퀴즈 풀기
                          </button>
                        </div>
                      </div>
                    ) : quizQuestions.length > 0 ? (
                      <div className="quiz-container">
                        <div className="quiz-progress">
                          <div className="progress-bar">
                            <div 
                              className="progress-fill" 
                              style={{ width: `${Math.min(((currentQuestionIndex + 1) / quizQuestions.length) * 100, 100)}%` }}
                            />
                          </div>
                          <span className="progress-text">
                            {Math.min(currentQuestionIndex + 1, quizQuestions.length)} / {quizQuestions.length}
                          </span>
                        </div>
                        
                        <div className="quiz-question-card">
                          <div className="question-header">
                            <span className="question-type-badge">
                              {quizMode === 'ox' ? 'OX형' : '단답형'}
                            </span>
                            <span className="question-number-large">Q{Math.min(currentQuestionIndex + 1, quizQuestions.length)}</span>
                          </div>
                          <div className="question-text">
                            {quizQuestions[currentQuestionIndex]?.question || '문제를 불러오는 중...'}
                          </div>
                          
                          {/* 힌트 표시 */}
                          {showHint && quizQuestions[currentQuestionIndex]?.hint && (
                            <div className="quiz-hint-box">
                              <div className="hint-icon">💡</div>
                              <div className="hint-text">{quizQuestions[currentQuestionIndex].hint}</div>
                            </div>
                          )}
                          
                          {/* 정답 표시 */}
                          {showAnswer && (
                            <div className="quiz-answer-box">
                              <div className="answer-icon">✓</div>
                              <div className="answer-text">
                                <span className="answer-label-text">정답: </span>
                                <span className="answer-value">{quizQuestions[currentQuestionIndex]?.answer}</span>
                              </div>
                            </div>
                          )}
                          
                          {/* 힌트/정답 버튼 */}
                          <div className="quiz-help-buttons">
                            {quizQuestions[currentQuestionIndex]?.hint && (
                              <button
                                className="hint-button"
                                onClick={() => setShowHint(!showHint)}
                              >
                                {showHint ? '💡 힌트 숨기기' : '💡 힌트 보기'}
                              </button>
                            )}
                            <button
                              className="answer-button"
                              onClick={() => {
                                const newShowAnswer = !showAnswer
                                setShowAnswer(newShowAnswer)
                                // 정답 확인 시 자동으로 답안 입력란에 정답 채우기
                                if (newShowAnswer && quizQuestions[currentQuestionIndex]) {
                                  const currentAnswer = quizQuestions[currentQuestionIndex].answer
                                  if (quizMode === 'ox') {
                                    setUserAnswer(currentAnswer.toUpperCase())
                                  } else {
                                    setUserAnswer(currentAnswer)
                                  }
                                }
                              }}
                            >
                              {showAnswer ? '✓ 정답 숨기기' : '✓ 정답 확인'}
                            </button>
                          </div>
                          
                          {quizMode === 'ox' ? (
                            <div className="ox-answers">
                              <button
                                className={`ox-button ${userAnswer === 'O' ? 'selected' : ''}`}
                                onClick={() => setUserAnswer('O')}
                              >
                                O (맞음)
                              </button>
                              <button
                                className={`ox-button ${userAnswer === 'X' ? 'selected' : ''}`}
                                onClick={() => setUserAnswer('X')}
                              >
                                X (틀림)
                              </button>
                            </div>
                          ) : (
                            <div className="short-answer-input">
                              <input
                                type="text"
                                className="answer-input"
                                placeholder="답을 입력하세요"
                                value={userAnswer}
                                onChange={(e) => setUserAnswer(e.target.value)}
                                onKeyPress={(e) => {
                                  if (e.key === 'Enter') {
                                    handleSubmitAnswer()
                                  }
                                }}
                              />
                            </div>
                          )}
                          
                          <button
                            className="submit-answer-button"
                            onClick={handleSubmitAnswer}
                            disabled={!userAnswer.trim()}
                          >
                            {currentQuestionIndex < quizQuestions.length - 1 ? '다음 문제 →' : '제출하기 ✓'}
                          </button>
                        </div>
                        
                        <div className="quiz-score-mini">
                          현재 점수: {quizScore.correct} / {currentQuestionIndex} {currentQuestionIndex > 0 && quizScore.correct > 0 ? `(${Math.round((quizScore.correct / currentQuestionIndex) * 100)}%)` : ''}
                        </div>
                      </div>
                    ) : (
                      <div className="loading-state">
                        <span className="spinner"></span>
                        <p>퀴즈 문제를 생성하는 중...</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ClassicMusicEducation

