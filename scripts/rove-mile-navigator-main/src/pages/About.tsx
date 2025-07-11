
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Plane, Users, BookOpen, Code, ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";

const About = () => {
  const navigate = useNavigate();

  const teamMembers = [
    { name: "Arya Sheth", role: "Project Lead", avatar: "AS" },
    { name: "Ali Salman", role: "Data Analyst", avatar: "AS" },
    { name: "Ciana Tzou", role: "Frontend Developer", avatar: "CT" },
    { name: "Kaushal Reddy Duddugunta", role: "Backend Engineer", avatar: "KD" },
    { name: "Norrissa Cole", role: "UX Researcher", avatar: "NC" },
    { name: "Prahas Duggireddy", role: "Data Scientist", avatar: "PD" },
    { name: "Shailesh", role: "Systems Architect", avatar: "S" }
  ];

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
              <Plane className="h-8 w-8 text-cyan-400" />
              <span className="text-xl font-bold text-white">Rove Rewards</span>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            About Our Project
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Rove Rewards Redemption Optimizer is a student-led internship project designed to help travelers 
            maximize the value of their airline miles and points through intelligent analysis and synthetic routing.
          </p>
        </div>

        {/* Technical Overview */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          <Card className="bg-white/10 backdrop-blur-lg border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <BookOpen className="w-6 h-6 mr-2 text-cyan-400" />
                GDS vs NDC Systems
              </CardTitle>
            </CardHeader>
            <CardContent className="text-slate-300">
              <p className="mb-4">
                Our research compared traditional Global Distribution Systems (GDS) with modern New Distribution Capability (NDC) systems:
              </p>
              <ul className="space-y-2 text-sm">
                <li><strong>GDS:</strong> Legacy systems used by travel agents and booking sites. Limited fare options but established infrastructure.</li>
                <li><strong>NDC:</strong> Modern airline-direct systems offering dynamic pricing and ancillary services.</li>
                <li><strong>Our Approach:</strong> We analyze both systems to find the best redemption values across all available channels.</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-white/10 backdrop-blur-lg border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Code className="w-6 h-6 mr-2 text-cyan-400" />
                Synthetic Routing Logic
              </CardTitle>
            </CardHeader>
            <CardContent className="text-slate-300">
              <p className="mb-4">
                Synthetic routing is our innovative approach to finding hidden value in airline redemptions:
              </p>
              <ul className="space-y-2 text-sm">
                <li><strong>Layover Optimization:</strong> We identify strategic connection points that reduce overall mile requirements.</li>
                <li><strong>Multi-Carrier Analysis:</strong> Compare redemptions across different airline partnerships and alliances.</li>
                <li><strong>Value Calculation:</strong> Real-time analysis of cash prices vs. mile requirements to maximize your savings.</li>
              </ul>
            </CardContent>
          </Card>
        </div>

        {/* Technology Stack */}
        <Card className="bg-white/10 backdrop-blur-lg border-white/20 mb-16">
          <CardHeader>
            <CardTitle className="text-white text-center text-2xl">Our Technology Stack</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
              <div>
                <div className="bg-gradient-to-br from-blue-500 to-cyan-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Code className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-white font-semibold">Python Backend</h3>
                <p className="text-slate-400 text-sm">Data processing & algorithms</p>
              </div>
              <div>
                <div className="bg-gradient-to-br from-cyan-500 to-blue-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
                  <BookOpen className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-white font-semibold">SQLite Database</h3>
                <p className="text-slate-400 text-sm">Flight data storage</p>
              </div>
              <div>
                <div className="bg-gradient-to-br from-purple-500 to-pink-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Plane className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-white font-semibold">React Frontend</h3>
                <p className="text-slate-400 text-sm">Modern user interface</p>
              </div>
              <div>
                <div className="bg-gradient-to-br from-orange-500 to-red-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Users className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-white font-semibold">REST APIs</h3>
                <p className="text-slate-400 text-sm">Real-time data integration</p>
              </div>
            </div>
          </CardContent>
        </Card>


        {/* Team Section */}
        <Card className="bg-white/10 backdrop-blur-lg border-white/20">
          <CardHeader>
            <CardTitle className="text-white text-center text-2xl flex items-center justify-center">
              <Users className="w-6 h-6 mr-2 text-cyan-400" />
              Meet the Team
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {teamMembers.map((member, index) => (
                <div key={index} className="text-center">
                  <div className="bg-gradient-to-br from-cyan-500 to-blue-500 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-white font-bold text-xl">{member.avatar}</span>
                  </div>
                  <h3 className="text-white font-semibold text-lg">{member.name}</h3>
                  <p className="text-slate-400">{member.role}</p>
                </div>
              ))}
            </div>
            <div className="text-center mt-8">
              <p className="text-slate-300">
                This project was developed as part of the Rove Internship Program, 
                focusing on practical applications of data science and travel technology.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default About;
