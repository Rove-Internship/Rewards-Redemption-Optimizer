
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Checkbox } from "@/components/ui/checkbox";
import { ArrowLeft, Send, MessageSquare, Star } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";

const Feedback = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    rating: "",
    usageType: "",
    feedback: "",
    improvements: [] as string[],
    recommend: false
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Feedback submitted:", formData);
    
    toast({
      title: "Thank you for your feedback!",
      description: "Your input helps us improve the Rove Rewards experience.",
    });
    
    // Reset form
    setFormData({
      name: "",
      email: "",
      rating: "",
      usageType: "",
      feedback: "",
      improvements: [],
      recommend: false
    });
  };

  const handleImprovementChange = (improvement: string, checked: boolean) => {
    if (checked) {
      setFormData(prev => ({
        ...prev,
        improvements: [...prev.improvements, improvement]
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        improvements: prev.improvements.filter(item => item !== improvement)
      }));
    }
  };

  const getRatingStars = (rating: string) => {
    const numRating = parseInt(rating) || 0;
    return Array(5).fill(0).map((_, i) => (
      <Star 
        key={i} 
        className={`w-6 h-6 cursor-pointer transition-colors ${
          i < numRating ? 'text-yellow-400 fill-current' : 'text-gray-400 hover:text-yellow-300'
        }`}
        onClick={() => setFormData(prev => ({ ...prev, rating: (i + 1).toString() }))}
      />
    ));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Navigation */}
      <nav className="bg-white/10 backdrop-blur-lg border-b border-white/20 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Button 
                onClick={() => navigate("/")}
                variant="ghost" 
                className="text-white hover:text-cyan-400 hover:bg-white/10"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Home
              </Button>
            </div>
            <div className="flex items-center space-x-2">
              <MessageSquare className="h-8 w-8 text-cyan-400" />
              <span className="text-xl font-bold text-white">Feedback</span>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-16 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Share Your Experience
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Help us improve Rove Rewards by sharing your thoughts and suggestions. 
            Your feedback drives our development priorities.
          </p>
        </div>

        {/* Feedback Form */}
        <Card className="bg-white/10 backdrop-blur-lg border-white/20">
          <CardHeader>
            <CardTitle className="text-white text-2xl text-center">
              Tell Us What You Think
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Personal Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="name" className="text-white">Name (Optional)</Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                    className="bg-white/20 border-white/30 text-white placeholder:text-slate-400"
                    placeholder="Your name"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-white">Email (Optional)</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                    className="bg-white/20 border-white/30 text-white placeholder:text-slate-400"
                    placeholder="your.email@example.com"
                  />
                </div>
              </div>

              {/* Rating */}
              <div className="space-y-4">
                <Label className="text-white text-lg">Overall Rating</Label>
                <div className="flex items-center space-x-2">
                  {getRatingStars(formData.rating)}
                  <span className="text-slate-300 ml-4">
                    {formData.rating ? `${formData.rating}/5 stars` : 'Click to rate'}
                  </span>
                </div>
              </div>

              {/* Usage Type */}
              <div className="space-y-4">
                <Label className="text-white text-lg">How did you use Rove Rewards?</Label>
                <RadioGroup 
                  value={formData.usageType} 
                  onValueChange={(value) => setFormData(prev => ({ ...prev, usageType: value }))}
                  className="space-y-3"
                >
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="planning" id="planning" />
                    <Label htmlFor="planning" className="text-slate-300">Planning a future trip</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="booking" id="booking" />
                    <Label htmlFor="booking" className="text-slate-300">Ready to book immediately</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="research" id="research" />
                    <Label htmlFor="research" className="text-slate-300">Researching mile values</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="comparison" id="comparison" />
                    <Label htmlFor="comparison" className="text-slate-300">Comparing with other tools</Label>
                  </div>
                </RadioGroup>
              </div>

              {/* Main Feedback */}
              <div className="space-y-4">
                <Label htmlFor="feedback" className="text-white text-lg">Your Feedback</Label>
                <Textarea
                  id="feedback"
                  value={formData.feedback}
                  onChange={(e) => setFormData(prev => ({ ...prev, feedback: e.target.value }))}
                  className="bg-white/20 border-white/30 text-white placeholder:text-slate-400 min-h-[120px]"
                  placeholder="Tell us about your experience with Rove Rewards. What worked well? What could be improved?"
                  required
                />
              </div>

              {/* Improvement Suggestions */}
              <div className="space-y-4">
                <Label className="text-white text-lg">What features would you like to see improved?</Label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {[
                    "Search interface",
                    "Results display",
                    "Value calculations",
                    "Route visualization",
                    "Mobile experience",
                    "Loading speed",
                    "More airlines",
                    "Hotel redemptions"
                  ].map((improvement) => (
                    <div key={improvement} className="flex items-center space-x-2">
                      <Checkbox
                        id={improvement}
                        checked={formData.improvements.includes(improvement)}
                        onCheckedChange={(checked) => handleImprovementChange(improvement, checked as boolean)}
                      />
                      <Label htmlFor={improvement} className="text-slate-300">{improvement}</Label>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendation */}
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="recommend"
                  checked={formData.recommend}
                  onCheckedChange={(checked) => setFormData(prev => ({ ...prev, recommend: checked as boolean }))}
                />
                <Label htmlFor="recommend" className="text-slate-300">
                  I would recommend Rove Rewards to other travelers
                </Label>
              </div>

              {/* Submit Button */}
              <Button 
                type="submit"
                className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-semibold py-3 text-lg"
              >
                <Send className="w-5 h-5 mr-2" />
                Submit Feedback
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Additional Contact Info */}
        <div className="mt-12 text-center">
          <Card className="bg-white/10 backdrop-blur-lg border-white/20">
            <CardContent className="pt-6">
              <h3 className="text-white text-xl font-semibold mb-4">Other Ways to Reach Us</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-slate-300">
                <div>
                  <h4 className="font-medium text-cyan-400 mb-2">Email</h4>
                  <p>rove.team@internship.edu</p>
                </div>
                <div>
                  <h4 className="font-medium text-cyan-400 mb-2">GitHub</h4>
                  <p>github.com/rove-internship</p>
                </div>
                <div>
                  <h4 className="font-medium text-cyan-400 mb-2">Office Hours</h4>
                  <p>Mon-Fri, 10am-4pm EST</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Feedback;
