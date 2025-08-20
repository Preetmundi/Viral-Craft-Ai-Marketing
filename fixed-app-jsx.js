import React, { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, Sparkles, TrendingUp, Video, Zap } from 'lucide-react'
import './App.css'

function App() {
  const [prompt, setPrompt] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedVideo, setGeneratedVideo] = useState(null)
  const [error, setError] = useState(null)
  const [trendingElements, setTrendingElements] = useState([
    { type: 'sound', name: 'Viral Dance Beat #1', popularity: 95 },
    { type: 'effect', name: 'Neon Glow Transition', popularity: 88 },
    { type: 'meme', name: 'POV Format', popularity: 92 },
    { type: 'sound', name: 'Trending Audio Clip', popularity: 85 }
  ])

  // Configuration for API endpoint - defaults to local, can be changed for production
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000'

  // Mock trending data for fallback
  const TRENDING_SOUNDS = [
    "Viral Dance Beat #1", "Trending Audio Clip", "Popular Song Remix", 
    "Comedy Sound Effect", "Motivational Speech Clip"
  ]

  const TRENDING_EFFECTS = [
    "Neon Glow Transition", "Glitch Effect", "Zoom Blur", 
    "Color Pop Filter", "Vintage Film Look"
  ]

  const TRENDING_MEMES = [
    "POV Format", "Before/After", "Day in My Life", 
    "Rating Things", "Explaining to My Past Self"
  ]

  // Fallback function for when backend is unavailable
  const generateMockResponse = (userPrompt) => {
    const applied_trends = []
    
    // Randomly select trending elements to apply
    if (Math.random() > 0.3) {
      applied_trends.push(TRENDING_SOUNDS[Math.floor(Math.random() * TRENDING_SOUNDS.length)])
    }
    if (Math.random() > 0.4) {
      applied_trends.push(TRENDING_EFFECTS[Math.floor(Math.random() * TRENDING_EFFECTS.length)])
    }
    if (Math.random() > 0.5) {
      applied_trends.push(TRENDING_MEMES[Math.floor(Math.random() * TRENDING_MEMES.length)])
    }

    // Generate enhanced description
    let enhanced_description = `🎬 Enhanced version of your idea: "${userPrompt}"\n\n`
    enhanced_description += "🚀 AI Suggestions:\n"
    
    if (userPrompt.toLowerCase().includes("dance")) {
      enhanced_description += "• Add trending dance moves synchronized with popular beat\n"
      enhanced_description += "• Use quick cuts and zoom effects for dynamic feel\n"
      enhanced_description += "• Include mirror/split screen effects\n"
    } else if (userPrompt.toLowerCase().includes("food")) {
      enhanced_description += "• Include close-up shots with satisfying sound effects\n"
      enhanced_description += "• Add text overlay with ratings or reactions\n"
      enhanced_description += "• Use trending food styling techniques\n"
    } else if (userPrompt.toLowerCase().includes("tutorial")) {
      enhanced_description += "• Use step-by-step text overlays\n"
      enhanced_description += "• Add before/after comparison shots\n"
      enhanced_description += "• Include trending educational formats\n"
    } else if (userPrompt.toLowerCase().includes("pet") || userPrompt.toLowerCase().includes("dog") || userPrompt.toLowerCase().includes("cat")) {
      enhanced_description += "• Add cute pet reaction shots\n"
      enhanced_description += "• Use trending pet sounds and effects\n"
      enhanced_description += "• Include popular pet challenge formats\n"
    } else if (userPrompt.toLowerCase().includes("reaction")) {
      enhanced_description += "• Use split-screen reaction format\n"
      enhanced_description += "• Add trending reaction sounds\n"
      enhanced_description += "• Include emotional text overlays\n"
    } else {
      enhanced_description += "• Apply trending visual effects for engagement\n"
      enhanced_description += "• Include popular audio elements\n"
      enhanced_description += "• Use current meme formats\n"
    }
    
    enhanced_description += `\n✨ Trending elements applied: ${applied_trends.join(', ')}`
    enhanced_description += `\n📊 Estimated viral score: ${Math.floor(Math.random() * 20) + 75}%`
    enhanced_description += `\n🎯 Best platforms: TikTok, Instagram Reels, YouTube Shorts`

    return {
      success: true,
      description: enhanced_description,
      appliedTrends: applied_trends,
      estimatedViralScore: Math.floor(Math.random() * 20) + 75,
      suggestedPlatforms: ['TikTok', 'Instagram Reels', 'YouTube Shorts'],
      generatedAt: Date.now()
    }
  }

  const handleGenerate = async () => {
    if (!prompt.trim()) return
    
    setIsGenerating(true)
    setError(null)
    
    try {
      // Try to call the actual backend first
      const response = await fetch(`${API_BASE_URL}/api/generate-video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setGeneratedVideo(data)
      
    } catch (error) {
      console.warn('Backend unavailable, using offline mode:', error.message)
      
      // Fallback to mock response with realistic delay
      await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 1500))
      const mockResponse = generateMockResponse(prompt)
      setGeneratedVideo(mockResponse)
      
      // Show offline indicator
      setError('🔄 Running in offline mode - full features available when backend is connected')
    } finally {
      setIsGenerating(false)
    }
  }

  // Load trending elements from backend or use defaults
  const loadTrendingElements = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/trending-elements`)
      if (response.ok) {
        const data = await response.json()
        // Transform backend data to match frontend format
        const elements = [
          ...data.sounds.map(s => ({ type: 'sound', name: s.name, popularity: s.popularity })),
          ...data.effects.map(e => ({ type: 'effect', name: e.name, popularity: e.popularity })),
          ...data.memes.map(m => ({ type: 'meme', name: m.name, popularity: m.popularity }))
        ]
        setTrendingElements(elements)
      }
    } catch (error) {
      console.log('Using default trending elements')
      // Keep default trending elements
    }
  }

  // Load trending elements on component mount
  React.useEffect(() => {
    loadTrendingElements()
  }, [])

  const handleTrendClick = (trend) => {
    const examples = {
      'Viral Dance Beat #1': 'Create a fun dance video with my friends using the latest viral choreography',
      'Neon Glow Transition': 'Transform my room setup with glowing neon effects and smooth transitions',
      'POV Format': 'POV: You just discovered the perfect study routine that actually works',
      'Trending Audio Clip': 'React to trying the most popular food trend everyone is talking about',
      'Glitch Effect': 'Show my transformation using glitch effects and dramatic lighting',
      'Before/After': 'Before and after of organizing my entire closet in under 60 seconds'
    }
    
    if (examples[trend.name]) {
      setPrompt(examples[trend.name])
    } else {
      // Generate dynamic example based on trend type
      if (trend.type === 'sound') {
        setPrompt(`Create an engaging video using the ${trend.name} to showcase my daily routine`)
      } else if (trend.type === 'effect') {
        setPrompt(`Transform my space using ${trend.name} and trending visual styles`)
      } else {
        setPrompt(`Use the ${trend.name} format to share something interesting about my life`)
      }
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="h-8 w-8 text-yellow-400" />
            <h1 className="text-4xl font-bold text-white">ViralCraft AI</h1>
            <TrendingUp className="h-8 w-8 text-green-400" />
          </div>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Transform your ideas into viral short-form videos with AI-powered trend integration
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Creation Panel */}
          <div className="lg:col-span-2">
            <Card className="bg-white/10 backdrop-blur-md border-white/20">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Video className="h-5 w-5" />
                  Create Your Viral Video
                </CardTitle>
                <CardDescription className="text-gray-300">
                  Describe your video idea and let AI add trending elements
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <label className="text-white text-sm font-medium mb-2 block">
                    Video Concept
                  </label>
                  <Textarea
                    placeholder="e.g., A funny reaction to trying a new food trend, a quick tutorial on organizing your room, a dance challenge with my pet..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    className="bg-white/10 border-white/20 text-white placeholder:text-gray-400 min-h-[120px]"
                  />
                </div>
                
                <Button 
                  onClick={handleGenerate}
                  disabled={!prompt.trim() || isGenerating}
                  className="w-full bg-gradient-to-r from-pink-500 to-violet-500 hover:from-pink-600 hover:to-violet-600 text-white font-semibold py-3"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Generating Viral Content...
                    </>
                  ) : (
                    <>
                      <Zap className="mr-2 h-4 w-4" />
                      Generate Viral Video
                    </>
                  )}
                </Button>

                {/* Error/Status Display */}
                {error && (
                  <div className="p-4 bg-blue-500/20 border border-blue-500/30 rounded-lg">
                    <p className="text-blue-200 text-sm">{error}</p>
                  </div>
                )}

                {/* Generated Video Preview */}
                {generatedVideo && (
                  <div className="mt-6 p-6 bg-white/5 rounded-lg border border-white/10">
                    <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
                      <Sparkles className="h-4 w-4 text-yellow-400" />
                      Generated Video Concept
                    </h3>
                    <div className="space-y-4">
                      <div className="bg-gray-800/50 p-4 rounded-lg">
                        <pre className="text-gray-300 text-sm whitespace-pre-wrap font-sans">
                          {generatedVideo.description}
                        </pre>
                      </div>
                      
                      {generatedVideo.appliedTrends && generatedVideo.appliedTrends.length > 0 && (
                        <div>
                          <p className="text-white text-sm font-medium mb-2">Applied Trends:</p>
                          <div className="flex flex-wrap gap-2">
                            {generatedVideo.appliedTrends.map((trend, index) => (
                              <Badge key={index} className="bg-purple-600 text-white">
                                {trend}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div className="bg-green-600/20 p-3 rounded-lg">
                          <div className="text-green-400 font-medium">Viral Score</div>
                          <div className="text-green-300 text-lg">{generatedVideo.estimatedViralScore}%</div>
                        </div>
                        <div className="bg-blue-600/20 p-3 rounded-lg">
                          <div className="text-blue-400 font-medium">Best Platforms</div>
                          <div className="text-blue-300 text-xs">
                            {generatedVideo.suggestedPlatforms?.join(', ') || 'TikTok, Reels, Shorts'}
                          </div>
                        </div>
                      </div>
                      
                      <Button className="w-full bg-green-600 hover:bg-green-700">
                        Download Video Script & Assets
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Trending Elements Sidebar */}
          <div>
            <Card className="bg-white/10 backdrop-blur-md border-white/20">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-400" />
                  Trending Now
                </CardTitle>
                <CardDescription className="text-gray-300">
                  Hot elements being used in viral content
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {trendingElements.map((element, index) => (
                    <div 
                      key={index} 
                      className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10 cursor-pointer hover:bg-white/10 transition-colors"
                      onClick={() => handleTrendClick(element)}
                      title="Click to use as example"
                    >
                      <div>
                        <p className="text-white text-sm font-medium">{element.name}</p>
                        <p className="text-gray-400 text-xs capitalize">{element.type}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-green-400 text-sm font-bold">{element.popularity}%</div>
                        <div className="text-gray-400 text-xs">viral</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Features Card */}
            <Card className="bg-white/10 backdrop-blur-md border-white/20 mt-6">
              <CardHeader>
                <CardTitle className="text-white text-lg">Why ViralCraft?</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 text-sm">
                  <div className="flex items-center gap-2 text-gray-300">
                    <Sparkles className="h-4 w-4 text-yellow-400" />
                    AI-powered trend detection
                  </div>
                  <div className="flex items-center gap-2 text-gray-300">
                    <TrendingUp className="h-4 w-4 text-green-400" />
                    Real-time viral elements
                  </div>
                  <div className="flex items-center gap-2 text-gray-300">
                    <Video className="h-4 w-4 text-blue-400" />
                    Optimized for all platforms
                  </div>
                  <div className="flex items-center gap-2 text-gray-300">
                    <Zap className="h-4 w-4 text-purple-400" />
                    Instant content generation
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Tips */}
            <Card className="bg-white/10 backdrop-blur-md border-white/20 mt-6">
              <CardHeader>
                <CardTitle className="text-white text-lg">💡 Quick Tips</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm text-gray-300">
                  <p>• Click trending elements to get example prompts</p>
                  <p>• Be specific about your video concept</p>
                  <p>• Include emotions and actions for better results</p>
                  <p>• Mention your target platform for optimized suggestions</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App