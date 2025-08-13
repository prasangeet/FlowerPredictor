"use client";

import React, { useState, useRef } from "react";
import { useEffect } from 'react';
import { useTheme } from 'next-themes';
import axios from "axios";
import { Upload, Image as ImageIcon, Sparkles, AlertCircle, Check, Moon, Sun, Flower } from "lucide-react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [mounted, setMounted] = useState(false);
  const fileInputRef = useRef(null);
  
  const { theme, setTheme } = useTheme();

  // Handle hydration mismatch
  useEffect(() => {
    setMounted(true);
  }, []);

  const handleFileChange = (selectedFile) => {
    if (selectedFile && selectedFile.type.startsWith('image/')) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setPrediction(null);
      setError(null); 
    } else {
      setError("Please select a valid image file");
    }
  };

  const handleInputChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileChange(e.target.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileChange(droppedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/api/predict/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log(res.data);

      setPrediction(res.data);
    } catch (error) {
      console.error(error);
      setError("Failed to identify flower. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const resetUpload = () => {
    setFile(null);
    setPreview(null);
    setPrediction(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const toggleTheme = () => {
    if (theme === 'dark') {
      setTheme('light');
    } else {
      setTheme('dark');
    }
  };

  // Prevent hydration mismatch by not rendering theme-dependent content until mounted
  if (!mounted) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-rose-50 to-purple-50 dark:from-gray-900 dark:via-purple-900 dark:to-pink-900 transition-colors duration-300">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-grid-slate-100 dark:bg-grid-slate-800 [mask-image:linear-gradient(0deg,#fff,rgba(255,255,255,0.6))] dark:[mask-image:linear-gradient(0deg,#000,rgba(0,0,0,0.6))] -z-10" />
      
      {/* Dark Mode Toggle */}
      <div className="absolute top-6 right-6 z-10">
        <button
          onClick={toggleTheme}
          className="p-3 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-full shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? (
            <Sun className="w-5 h-5 text-yellow-500" />
          ) : (
            <Moon className="w-5 h-5 text-gray-700" />
          )}
        </button>
      </div>
      
      <div className="container mx-auto px-4 py-8 md:py-16">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-600 rounded-2xl mb-6 shadow-lg">
            <Flower className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-pink-600 via-purple-600 to-rose-800 dark:from-pink-400 dark:via-purple-400 dark:to-rose-400 bg-clip-text text-transparent mb-4">
            AI Flower Identifier
          </h1>
          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto leading-relaxed">
            Upload a flower image and discover its species. Powered by AI trained on the Oxford 102 flower dataset.
          </p>
          <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-pink-100 dark:bg-pink-900/30 rounded-full text-sm text-pink-700 dark:text-pink-300">
            <Sparkles className="w-4 h-4" />
            <span>Trained on Oxford 102 Dataset</span>
          </div>
        </div>

        <div className="max-w-4xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-8 lg:gap-12">
            {/* Upload Section */}
            <div className="space-y-6">
              <div className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 dark:border-gray-700/20 p-8">
                <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-6 flex items-center gap-2">
                  <Upload className="w-6 h-6 text-pink-600 dark:text-pink-400" />
                  Upload Flower Image
                </h2>
                
                {/* Drag & Drop Zone */}
                <div
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  className={`
                    relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer
                    transition-all duration-300 ease-in-out
                    ${isDragOver 
                      ? 'border-pink-500 bg-pink-50 dark:bg-pink-900/20 scale-105' 
                      : 'border-gray-300 dark:border-gray-600 hover:border-pink-400 dark:hover:border-pink-500 hover:bg-pink-50/50 dark:hover:bg-pink-900/10'
                    }
                  `}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    onChange={handleInputChange}
                    accept="image/*"
                    className="hidden"
                  />
                  
                  <div className="space-y-4">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-pink-100 to-purple-100 dark:from-pink-900/50 dark:to-purple-900/50 rounded-full">
                      <ImageIcon className="w-8 h-8 text-pink-600 dark:text-pink-400" />
                    </div>
                    <div>
                      <p className="text-lg font-semibold text-gray-700 dark:text-gray-300">
                        {isDragOver ? 'Drop your flower image here' : 'Click to upload or drag & drop'}
                      </p>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                        Supports JPG, PNG, GIF up to 10MB
                      </p>
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={handleUpload}
                    disabled={!file || loading}
                    className="
                      flex-1 flex items-center justify-center gap-2 px-6 py-3
                      bg-gradient-to-r from-pink-600 to-purple-600 text-white font-semibold
                      rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5
                      disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none
                      transition-all duration-200
                    "
                  >
                    {loading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                        Identifying...
                      </>
                    ) : (
                      <>
                        <Flower className="w-5 h-5" />
                        Identify Flower
                      </>
                    )}
                  </button>
                  
                  {(file || prediction || error) && (
                    <button
                      onClick={resetUpload}
                      className="
                        px-6 py-3 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-semibold
                        rounded-xl hover:border-gray-400 dark:hover:border-gray-500 hover:bg-gray-50 dark:hover:bg-gray-800
                        transition-all duration-200
                      "
                    >
                      Reset
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* Preview & Results Section */}
            <div className="space-y-6">
              {/* Image Preview */}
              {preview && (
                <div className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 dark:border-gray-700/20 p-8">
                  <h3 className="text-xl font-bold text-gray-800 dark:text-gray-200 mb-4">Preview</h3>
                  <div className="relative group">
                    <img 
                      src={preview} 
                      alt="Preview" 
                      className="w-full h-64 object-cover rounded-2xl shadow-lg transition-transform duration-300 group-hover:scale-105" 
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </div>
                </div>
              )}

              {/* Prediction Results */}
              {(prediction || error) && (
                <div className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 dark:border-gray-700/20 p-8">
                  <h3 className="text-xl font-bold text-gray-800 dark:text-gray-200 mb-4 flex items-center gap-2">
                    {prediction ? (
                      <>
                        <Check className="w-5 h-5 text-green-600 dark:text-green-400" />
                        Flower Identification
                      </>
                    ) : (
                      <>
                        <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
                        Error
                      </>
                    )}
                  </h3>
                  
                  {prediction && (
                    <div className="space-y-4">
                      <div className="bg-gradient-to-r from-green-50 to-pink-50 dark:from-green-900/20 dark:to-pink-900/20 rounded-2xl p-6 border border-green-100 dark:border-green-800/30">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-pink-500 rounded-full animate-pulse" />
                          <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Identified Flower</span>
                        </div>
                        <p className="text-2xl font-bold text-gray-800 dark:text-gray-200 flex items-center gap-2">
                          <Flower className="w-6 h-6 text-pink-500" />
                          {prediction?.class}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                          From Oxford 102 Flower Dataset
                        </p>
                      </div>
                    </div>
                  )}
                  
                  {error && (
                    <div className="bg-red-50 dark:bg-red-900/20 rounded-2xl p-6 border border-red-100 dark:border-red-800/30">
                      <p className="text-red-800 dark:text-red-400 font-medium">{error}</p>
                    </div>
                  )}
                </div>
              )}

              {/* Info Card */}
              {!preview && !prediction && !error && (
                <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-3xl shadow-lg border border-white/20 dark:border-gray-700/20 p-8">
                  <h3 className="text-xl font-bold text-gray-800 dark:text-gray-200 mb-4">How it works</h3>
                  <div className="space-y-4 text-gray-600 dark:text-gray-400">
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-pink-100 dark:bg-pink-900/50 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-pink-600 dark:text-pink-400 font-bold text-sm">1</span>
                      </div>
                      <p>Upload or drag & drop your flower image</p>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-purple-100 dark:bg-purple-900/50 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-purple-600 dark:text-purple-400 font-bold text-sm">2</span>
                      </div>
                      <p>AI analyzes the flower using Oxford 102 dataset</p>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-green-100 dark:bg-green-900/50 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-green-600 dark:text-green-400 font-bold text-sm">3</span>
                      </div>
                      <p>Get instant flower species identification</p>
                    </div>
                  </div>
                  
                  <div className="mt-6 p-4 bg-gradient-to-r from-pink-50 to-purple-50 dark:from-pink-900/20 dark:to-purple-900/20 rounded-xl border border-pink-100 dark:border-pink-800/30">
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      <strong className="text-pink-600 dark:text-pink-400">Oxford 102 Dataset:</strong> Contains 102 flower categories with 40-258 images per category, including popular flowers like roses, tulips, daisies, and many rare species.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}