"use client";

import React, { useState, useRef, useEffect } from "react";
import { useTheme } from "next-themes";
import axios from "axios";
import {
  Upload,
  Image as ImageIcon,
  Sparkles,
  AlertCircle,
  Check,
  Moon,
  Sun,
  Flower,
  RefreshCw,
  Info,
} from "lucide-react";

// Shadcn UI Component Imports
// Assuming standard path @/components/ui/...
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";

export default function Home() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [mounted, setMounted] = useState(false);
  const fileInputRef = useRef(null);

  const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

  const { theme, setTheme } = useTheme();

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleFileChange = (selectedFile) => {
    if (selectedFile && selectedFile.type.startsWith("image/")) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setPrediction(null);
      setError(null);
    } else {
      setError("Please select a valid image file (JPG, PNG)");
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
    formData.append("image", file); // MUST be "image"

    try {
      const res = await axios.post(`${BASE_URL}/predict`, formData, {
        headers: {
          Accept: "application/json",
          // ❌ DO NOT SET Content-Type
        },
      });

      setPrediction(res.data);
      console.log(res.data);
    } catch (err) {
      console.error(err.response?.data || err);
      setError("Failed to identify flower");
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
    setTheme(theme === "dark" ? "light" : "dark");
  };

  if (!mounted) {
    return <div className="min-h-screen bg-background" />;
  }

  return (
    <div className="min-h-screen bg-background transition-colors duration-300">
      {/* Abstract Background */}
      <div className="fixed inset-0 -z-10 h-full w-full bg-white dark:bg-slate-950 [background:radial-gradient(125%_125%_at_50%_10%,#fff_40%,#ff007a_100%)] dark:[background:radial-gradient(125%_125%_at_50%_10%,#000_40%,#63e_100%)] opacity-20" />

      <div className="container mx-auto px-4 py-8 md:py-12 max-w-6xl">
        {/* Top Navigation / Header */}
        <div className="flex justify-between items-center mb-12">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Flower className="w-6 h-6 text-primary" />
            </div>
            <span className="font-bold text-xl tracking-tight">FloraAI</span>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            className="rounded-full"
          >
            {theme === "dark" ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </Button>
        </div>

        <div className="grid lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Title & Upload */}
          <div className="lg:col-span-5 space-y-6">
            <div className="space-y-4">
              <Badge
                variant="secondary"
                className="px-3 py-1 text-primary bg-primary/10 hover:bg-primary/20 border-primary/20"
              >
                <Sparkles className="w-3 h-3 mr-1" />
                V2.0 Model • Oxford 102
              </Badge>
              <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight lg:text-6xl">
                Identify flowers <br />
                <span className="text-primary">instantly.</span>
              </h1>
              <p className="text-muted-foreground text-lg">
                Upload a photo and let our neural network identify the species
                with high accuracy.
              </p>
              [Image of Convolutional Neural Network architecture]
            </div>

            <Card className="border-2 border-dashed shadow-none bg-background/50 backdrop-blur-sm">
              <CardContent className="pt-6">
                <div
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  className={`
                    relative rounded-xl p-10 text-center cursor-pointer transition-all duration-300
                    ${
                      isDragOver
                        ? "bg-primary/5 ring-2 ring-primary ring-offset-2"
                        : "hover:bg-muted/50"
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
                  <div className="flex flex-col items-center gap-4">
                    <div
                      className={`p-4 rounded-full transition-colors ${isDragOver ? "bg-primary/20 text-primary" : "bg-muted text-muted-foreground"}`}
                    >
                      <Upload className="w-8 h-8" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">
                        {isDragOver ? "Drop it here!" : "Click or Drag Image"}
                      </h3>
                      <p className="text-sm text-muted-foreground mt-1">
                        Supports JPG, PNG up to 10MB
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="flex gap-4">
              <Button
                size="lg"
                className="flex-1 text-md font-semibold"
                onClick={handleUpload}
                disabled={!file || loading}
              >
                {loading ? (
                  <>
                    <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Identify Flower
                  </>
                )}
              </Button>
              {(file || prediction) && (
                <Button variant="outline" size="lg" onClick={resetUpload}>
                  Reset
                </Button>
              )}
            </div>
          </div>

          {/* Right Column: Preview & Results */}
          <div className="lg:col-span-7">
            <Card className="h-full min-h-[500px] flex flex-col overflow-hidden border-muted shadow-xl">
              <CardHeader className="border-b bg-muted/30">
                <CardTitle className="flex items-center gap-2">
                  <ImageIcon className="w-5 h-5" />
                  Analysis Dashboard
                </CardTitle>
              </CardHeader>

              <CardContent className="flex-1 p-0 relative bg-muted/10">
                {!preview ? (
                  <div className="h-full flex flex-col items-center justify-center p-12 text-muted-foreground">
                    <Flower className="w-16 h-16 mb-4 opacity-20" />
                    <p>No image selected</p>
                    <p className="text-sm">
                      Upload an image to see results here
                    </p>
                  </div>
                ) : (
                  <div className="relative h-full flex flex-col">
                    {/* Image Container */}
                    <div className="relative w-full h-80 bg-black/5 dark:bg-black/50">
                      <img
                        src={preview}
                        alt="Preview"
                        className="w-full h-full object-contain p-4"
                      />
                    </div>

                    {/* Results Container */}
                    <div className="flex-1 p-6 bg-background border-t">
                      {loading ? (
                        <div className="space-y-4">
                          <div className="flex items-center gap-4">
                            <Skeleton className="h-12 w-12 rounded-full" />
                            <div className="space-y-2">
                              <Skeleton className="h-4 w-[200px]" />
                              <Skeleton className="h-4 w-[150px]" />
                            </div>
                          </div>
                          <Skeleton className="h-24 w-full rounded-xl" />
                        </div>
                      ) : error ? (
                        <Alert variant="destructive">
                          <AlertCircle className="h-4 w-4" />
                          <AlertTitle>Error</AlertTitle>
                          <AlertDescription>{error}</AlertDescription>
                        </Alert>
                      ) : prediction ? (
                        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                          <div className="flex items-start justify-between">
                            <div>
                              <p className="text-sm font-medium text-muted-foreground mb-1">
                                Identified Species
                              </p>
                              <h2 className="text-3xl font-bold text-primary flex items-center gap-2">
                                {prediction?.predicted_class}
                                <Check className="w-6 h-6 text-green-500" />
                              </h2>
                            </div>
                            <Badge
                              variant="outline"
                              className="text-green-600 border-green-200 bg-green-50 dark:bg-green-900/20"
                            >
                              High Confidence
                            </Badge>
                          </div>

                          <Separator />

                          <div className="grid grid-cols-2 gap-4">
                            <div className="p-4 rounded-lg bg-muted/50 border">
                              <div className="flex items-center gap-2 mb-2 text-muted-foreground">
                                <Info className="w-4 h-4" />
                                <span className="text-sm font-medium">
                                  Dataset
                                </span>
                              </div>
                              <p className="font-medium">Oxford 102</p>
                            </div>
                            <div className="p-4 rounded-lg bg-muted/50 border">
                              <div className="flex items-center gap-2 mb-2 text-muted-foreground">
                                <ImageIcon className="w-4 h-4" />
                                <span className="text-sm font-medium">
                                  Resolution
                                </span>
                              </div>
                              <p className="font-medium">Original Quality</p>
                            </div>
                          </div>

                          <Alert className="bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-900/20 dark:text-blue-200 dark:border-blue-800">
                            <Sparkles className="h-4 w-4" />
                            <AlertTitle>Did you know?</AlertTitle>
                            <AlertDescription className="text-xs mt-1">
                              This AI analyzes petal texture, color gradients,
                              and stamen patterns to distinguish between 102
                              unique flower categories.
                            </AlertDescription>
                          </Alert>
                        </div>
                      ) : (
                        <div className="flex items-center justify-center h-full text-muted-foreground text-sm italic">
                          Ready to identify...
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
