
import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ArrowLeft, Plane, Star, DollarSign, Clock, ArrowRight } from "lucide-react";

// Mock data generator for redemption options
const generateMockResults = (origin: string, destination: string, miles: string) => {
  const baseValue = Math.random() * 0.02 + 0.01; // Random value between 1-3 cents per mile
  
  return [
    {
      id: 1,
      type: "Direct Flight",
      route: `${origin} → ${destination}`,
      milesRequired: parseInt(miles) * 0.8,
      cashPrice: 650,
      valuePerMile: baseValue * 1.2,
      fees: 25,
      airline: "Delta",
      duration: "5h 30m",
      savings: 520,
      rating: 5
    },
    {
      id: 2,
      type: "Synthetic Route",
      route: `${origin} → DXB → ${destination}`,
      milesRequired: parseInt(miles) * 0.6,
      cashPrice: 750,
      valuePerMile: baseValue * 1.5,
      fees: 45,
      airline: "Emirates",
      duration: "12h 15m",
      savings: 705,
      rating: 4
    },
    {
      id: 3,
      type: "Direct Flight",
      route: `${origin} → ${destination}`,
      milesRequired: parseInt(miles) * 0.9,
      cashPrice: 580,
      valuePerMile: baseValue * 0.9,
      fees: 35,
      airline: "United",
      duration: "5h 45m",
      savings: 545,
      rating: 4
    },
    {
      id: 4,
      type: "Synthetic Route",
      route: `${origin} → CDG → ${destination}`,
      milesRequired: parseInt(miles) * 0.7,
      cashPrice: 680,
      valuePerMile: baseValue * 1.3,
      fees: 55,
      airline: "Air France",
      duration: "10h 20m",
      savings: 625,
      rating: 4
    }
  ].sort((a, b) => b.valuePerMile - a.valuePerMile);
};

const Results = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [results, setResults] = useState<any[]>([]);
  const [filter, setFilter] = useState("value");

  const origin = searchParams.get("origin");
  const destination = searchParams.get("destination");
  const departDate = searchParams.get("departDate");
  const miles = searchParams.get("miles");

  useEffect(() => {
    if (origin && destination && miles) {
      const mockResults = generateMockResults(origin, destination, miles);
      setResults(mockResults);
    }
  }, [origin, destination, miles]);

  const filteredResults = results.sort((a, b) => {
    if (filter === "value") return b.valuePerMile - a.valuePerMile;
    if (filter === "fees") return a.fees - b.fees;
    if (filter === "savings") return b.savings - a.savings;
    return 0;
  });

  const getRatingStars = (rating: number) => {
    return Array(5).fill(0).map((_, i) => (
      <Star key={i} className={`w-4 h-4 ${i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} />
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
                Back to Search
              </Button>
            </div>
            <div className="flex items-center space-x-2">
              <Plane className="h-8 w-8 text-cyan-400" />
              <span className="text-xl font-bold text-white">Rove Rewards</span>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        {/* Search Summary */}
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 mb-8 border border-white/20">
          <h1 className="text-2xl font-bold text-white mb-4">
            Redemption Options: {origin} → {destination}
          </h1>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-slate-400">Departure:</span>
              <p className="text-white font-medium">{departDate}</p>
            </div>
            <div>
              <span className="text-slate-400">Miles Available:</span>
              <p className="text-white font-medium">{miles?.toLocaleString()}</p>
            </div>
            <div>
              <span className="text-slate-400">Options Found:</span>
              <p className="text-white font-medium">{results.length} redemptions</p>
            </div>
            <div>
              <span className="text-slate-400">Best Value:</span>
              <p className="text-white font-medium">
                {results[0]?.valuePerMile ? `${(results[0].valuePerMile * 100).toFixed(2)}¢/mile` : 'Loading...'}
              </p>
            </div>
          </div>
        </div>

        {/* Filter Tabs */}
        <Tabs value={filter} onValueChange={setFilter} className="mb-8">
          <TabsList className="bg-white/10 backdrop-blur-lg border border-white/20">
            <TabsTrigger value="value" className="data-[state=active]:bg-cyan-500">
              Maximize Value
            </TabsTrigger>
            <TabsTrigger value="fees" className="data-[state=active]:bg-cyan-500">
              Minimize Fees
            </TabsTrigger>
            <TabsTrigger value="savings" className="data-[state=active]:bg-cyan-500">
              Maximum Savings
            </TabsTrigger>
          </TabsList>

          <TabsContent value={filter} className="mt-6">
            <div className="grid gap-6">
              {filteredResults.map((result, index) => (
                <Card key={result.id} className="bg-white/10 backdrop-blur-lg border-white/20 hover:bg-white/15 transition-all duration-300">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <Badge variant={index === 0 ? "default" : "secondary"} className={index === 0 ? "bg-gradient-to-r from-cyan-500 to-blue-500" : ""}>
                          {index === 0 ? "Best Value" : `#${index + 1}`}
                        </Badge>
                        <CardTitle className="text-white text-lg">
                          {result.type} - {result.airline}
                        </CardTitle>
                        <div className="flex space-x-1">
                          {getRatingStars(result.rating)}
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-cyan-400">
                          {(result.valuePerMile * 100).toFixed(2)}¢
                        </p>
                        <p className="text-sm text-slate-400">per mile</p>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                      <div className="flex items-center space-x-2">
                        <Plane className="w-5 h-5 text-cyan-400" />
                        <div>
                          <p className="text-white font-medium">{result.route}</p>
                          <p className="text-sm text-slate-400">{result.duration}</p>
                        </div>
                      </div>
                      
                      <div className="text-center">
                        <p className="text-xl font-bold text-white">
                          {result.milesRequired.toLocaleString()}
                        </p>
                        <p className="text-sm text-slate-400">miles required</p>
                      </div>
                      
                      <div className="text-center">
                        <div className="flex items-center justify-center space-x-2">
                          <DollarSign className="w-4 h-4 text-green-400" />
                          <span className="text-xl font-bold text-green-400">
                            ${result.savings}
                          </span>
                        </div>
                        <p className="text-sm text-slate-400">saved vs cash (${result.cashPrice})</p>
                      </div>
                      
                      <div className="text-center">
                        <p className="text-lg font-medium text-orange-400">
                          +${result.fees}
                        </p>
                        <p className="text-sm text-slate-400">fees</p>
                      </div>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-white/20">
                      <Button className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600">
                        Book This Option
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>

        {/* Additional Info */}
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 border border-white/20">
          <h3 className="text-lg font-semibold text-white mb-4">Understanding Your Results</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            <div>
              <h4 className="font-medium text-cyan-400 mb-2">Direct Flights</h4>
              <p className="text-slate-300">
                Non-stop routes that get you there fastest. Usually require more miles but offer convenience and time savings.
              </p>
            </div>
            <div>
              <h4 className="font-medium text-cyan-400 mb-2">Synthetic Routes</h4>
              <p className="text-slate-300">
                Strategic layover combinations that can offer better value-per-mile ratios. Takes longer but maximizes your rewards.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
