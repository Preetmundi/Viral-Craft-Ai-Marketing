import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, Sparkles, TrendingUp, Video, Zap } from 'lucide-react'
import './App.css'

function App() {
  const [prompt, setPrompt] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedVideo, setGeneratedVideo] = useState(null)
  const [trendingElements, setTrendingElements] = useState([
    { type: 'sound', name: 'Viral Dance Beat #1', popularity: 95 },
    { type: 'effect', name: 'Neon Glow Transition', popularity: 88 },
    { type: 'meme', name: 'POV Format', popularity: 92 },
    { type: 'sound', name: 'Trending Audio Clip', popularity: 85 }
  ])

  const handleGenerate = async () => {
    if (!prompt.trim()) return
    
    setIsGenerating(true)
    
    try {
      const response = await fetch('http://localhost:5000/api/generate-video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      })
      
      const data = await response.json()
      setGeneratedVideo(data)
    } catch (error) {
      console.error('Error generating video:', error)
    } finally {
      setIsGenerating(false)
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

                {/* Generated Video Preview */}
                {generatedVideo && (
                  <div className="mt-6 p-4 bg-white/5 rounded-lg border border-white/10">
                    <h3 className="text-white font-semibold mb-3">Generated Video Concept</h3>
                    <div className="space-y-3">
                      <div className="bg-gray-800 p-3 rounded">
                        <p className="text-gray-300 text-sm">{generatedVideo.description}</p>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {generatedVideo.appliedTrends?.map((trend, index) => (
                          <Badge key={index} variant="secondary" className="bg-purple-600 text-white">
                            {trend}
                          </Badge>
                        ))}
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
                    <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
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
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

