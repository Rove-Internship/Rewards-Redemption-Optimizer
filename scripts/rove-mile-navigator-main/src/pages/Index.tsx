
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { CalendarIcon, Plane, MapPin, Calculator } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";
import { useNavigate } from "react-router-dom";

const popularRoutes = [
  { code: "BOS", city: "Boston", country: "USA" },
  { code: "SFO", city: "San Francisco", country: "USA" },
  { code: "JFK", city: "New York", country: "USA" },
  { code: "LHR", city: "London", country: "UK" },
  { code: "LAX", city: "Los Angeles", country: "USA" },
  { code: "HND", city: "Tokyo", country: "Japan" },
  { code: "CDG", city: "Paris", country: "France" },
  { code: "DXB", city: "Dubai", country: "UAE" },
];

const Index = () => {
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [departDate, setDepartDate] = useState<Date>();
  const [returnDate, setReturnDate] = useState<Date>();
  const [miles, setMiles] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (origin && destination && departDate && miles) {
      const searchParams = new URLSearchParams({
        origin,
        destination,
        departDate: departDate.toISOString().split('T')[0],
        returnDate: returnDate ? returnDate.toISOString().split('T')[0] : '',
        miles
      });
      navigate(`/results?${searchParams.toString()}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Navigation */}
      <nav className="bg-white/10 backdrop-blur-lg border-b border-white/20 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Plane className="h-8 w-8 text-cyan-400" />
              <span className="text-xl font-bold text-white">Rove Rewards</span>
            </div>
            <div className="hidden md:flex space-x-6">
              <a href="/" className="text-white hover:text-cyan-400 transition-colors">Home</a>
              <a href="/about" className="text-white hover:text-cyan-400 transition-colors">About</a>
              <a href="/feedback" className="text-white hover:text-cyan-400 transition-colors">Feedback</a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
            Rove Rewards
          </h1>
          <h2 className="text-3xl md:text-4xl font-semibold text-white mb-4">
            Redemption Optimizer
          </h2>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Get the most value from your miles. Smart routing, better rewards, maximum savings.
          </p>
        </div>

        {/* Search Form */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
              {/* Origin */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-white flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  From
                </label>
                <Select value={origin} onValueChange={setOrigin}>
                  <SelectTrigger className="bg-white/20 border-white/30 text-white">
                    <SelectValue placeholder="Select origin" />
                  </SelectTrigger>
                  <SelectContent>
                    {popularRoutes.map((route) => (
                      <SelectItem key={route.code} value={route.code}>
                        {route.code} - {route.city}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Destination */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-white flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  To
                </label>
                <Select value={destination} onValueChange={setDestination}>
                  <SelectTrigger className="bg-white/20 border-white/30 text-white">
                    <SelectValue placeholder="Select destination" />
                  </SelectTrigger>
                  <SelectContent>
                    {popularRoutes.map((route) => (
                      <SelectItem key={route.code} value={route.code}>
                        {route.code} - {route.city}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Miles Available */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-white flex items-center">
                  <Calculator className="w-4 h-4 mr-1" />
                  Miles Available
                </label>
                <Input
                  type="number"
                  placeholder="e.g. 50000"
                  value={miles}
                  onChange={(e) => setMiles(e.target.value)}
                  className="bg-white/20 border-white/30 text-white placeholder:text-slate-400"
                />
              </div>

              {/* Departure Date */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-white flex items-center">
                  <CalendarIcon className="w-4 h-4 mr-1" />
                  Departure
                </label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      className={cn(
                        "w-full justify-start text-left font-normal bg-white/20 border-white/30 text-white hover:bg-white/30",
                        !departDate && "text-slate-400"
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {departDate ? format(departDate, "PPP") : "Select date"}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      mode="single"
                      selected={departDate}
                      onSelect={setDepartDate}
                      initialFocus
                      className="pointer-events-auto"
                    />
                  </PopoverContent>
                </Popover>
              </div>

              {/* Return Date */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-white flex items-center">
                  <CalendarIcon className="w-4 h-4 mr-1" />
                  Return (Optional)
                </label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      className={cn(
                        "w-full justify-start text-left font-normal bg-white/20 border-white/30 text-white hover:bg-white/30",
                        !returnDate && "text-slate-400"
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {returnDate ? format(returnDate, "PPP") : "Select date"}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      mode="single"
                      selected={returnDate}
                      onSelect={setReturnDate}
                      initialFocus
                      className="pointer-events-auto"
                    />
                  </PopoverContent>
                </Popover>
              </div>
            </div>

            <Button 
              onClick={handleSearch}
              className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-semibold py-3 text-lg"
              disabled={!origin || !destination || !departDate || !miles}
            >
              Find Best Redemptions
            </Button>
          </div>
        </div>

        {/* Features Preview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 max-w-6xl mx-auto">
          <div className="text-center">
            <div className="bg-gradient-to-br from-cyan-500 to-blue-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Calculator className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Smart Value Calculator</h3>
            <p className="text-slate-300">Get precise value-per-mile calculations for every redemption option</p>
          </div>
          <div className="text-center">
            <div className="bg-gradient-to-br from-purple-500 to-pink-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Plane className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Synthetic Routing</h3>
            <p className="text-slate-300">Discover hidden layover combinations that maximize your savings</p>
          </div>
          <div className="text-center">
            <div className="bg-gradient-to-br from-orange-500 to-red-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <MapPin className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Multiple Options</h3>
            <p className="text-slate-300">Compare flights, hotels, and gift card redemptions side by side</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-black/20 backdrop-blur-lg border-t border-white/10 py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-slate-400">
            Built by the Rove Student Team for the Internship Project
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
