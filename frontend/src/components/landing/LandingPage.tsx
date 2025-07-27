"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, CheckCircle2, ExternalLink, Film, Sparkles, TrendingUp, Star } from "lucide-react";
import Link from "next/link";
import { BackgroundGradientAnimation } from "@/components/ui/background-gradient-animation";

export default function LandingPage() {
  const [isLoaded, setIsLoaded] = useState(false);

  const features = [
    {
      icon: <Sparkles className="w-5 h-5" />,
      title: "AI-Powered Recommendations",
      description: "Get personalized movie and TV show suggestions based on your mood and preferences"
    },
    {
      icon: <Film className="w-5 h-5" />,
      title: "Vast Entertainment Library",
      description: "Access information about thousands of movies and TV shows from various genres"
    },
    {
      icon: <TrendingUp className="w-5 h-5" />,
      title: "Real-time Trending Content",
      description: "Stay updated with what's popular and trending in the entertainment world"
    },
    {
      icon: <Star className="w-5 h-5" />,
      title: "Detailed Ratings & Reviews",
      description: "Make informed decisions with comprehensive ratings and user reviews"
    }
  ];

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Animated Background */}
      <BackgroundGradientAnimation
        gradientBackgroundStart="rgb(15, 23, 42)"
        gradientBackgroundEnd="rgb(30, 41, 59)"
        firstColor="59, 130, 246"
        secondColor="139, 92, 246"
        thirdColor="236, 72, 153"
        fourthColor="34, 197, 94"
        fifthColor="251, 146, 60"
        size="60%"
        containerClassName="absolute inset-0"
      />

      {/* Content */}
      <div className="relative z-10">
        {/* Navigation */}
        <nav className="bg-black/20 backdrop-blur-xl border-b border-white/10">
          <div className="container mx-auto px-6 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-xl">
                <Film className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-white">StreamSage AI</span>
            </div>
            <Link href="/chat">
              <Button className="bg-white/10 backdrop-blur-md hover:bg-white/20 text-white border border-white/20">
                Try Now
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="container mx-auto px-6 py-20 md:py-32">
          <div className="max-w-5xl mx-auto text-center space-y-8">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={isLoaded ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20"
            >
              <span className="flex h-2 w-2 rounded-full bg-green-400 animate-pulse"></span>
              <span className="text-sm font-medium text-white">AI-Powered Entertainment Discovery</span>
            </motion.div>

            {/* Main Heading */}
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={isLoaded ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="text-5xl md:text-7xl font-bold text-white leading-tight"
            >
              Discover Your Next
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400"> Favorite </span>
              Movie or Show
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              initial={{ opacity: 0, y: 30 }}
              animate={isLoaded ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.7, delay: 0.4 }}
              className="text-xl text-gray-300 max-w-3xl mx-auto"
            >
              Let our AI understand your mood and preferences to recommend the perfect entertainment for any moment. 
              From heartwarming comedies to thrilling adventures, find exactly what you're looking for.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={isLoaded ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.7, delay: 0.6 }}
              className="flex flex-wrap gap-4 justify-center"
            >
              <Link href="/chat">
                <Button size="lg" className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white px-8 py-6 text-lg shadow-lg">
                  Start Chatting
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Button 
                size="lg" 
                variant="outline" 
                className="bg-white/5 backdrop-blur-md hover:bg-white/10 text-white border-white/20 px-8 py-6 text-lg"
              >
                Learn More
                <ExternalLink className="ml-2 h-5 w-5" />
              </Button>
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={isLoaded ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          >
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={isLoaded ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.5, delay: 1 + index * 0.1 }}
                className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all duration-300"
              >
                <div className="text-cyan-400 mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-400 text-sm">{feature.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </section>

        {/* Stats Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={isLoaded ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, delay: 1.2 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto"
          >
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">50K+</div>
              <div className="text-gray-400">Movies & Shows</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">98%</div>
              <div className="text-gray-400">Accuracy Rate</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-white mb-2">24/7</div>
              <div className="text-gray-400">AI Assistant</div>
            </div>
          </motion.div>
        </section>
      </div>
    </div>
  );
}
