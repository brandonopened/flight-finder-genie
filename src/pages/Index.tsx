import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const Index = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string>("");
  const { toast } = useToast();

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/search-flight", {
        method: "POST",
      });
      
      if (!response.ok) {
        throw new Error("Failed to search flight");
      }
      
      const data = await response.text();
      setResult(data);
      toast({
        title: "Search completed",
        description: "Flight results have been found!",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to search for flights. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="max-w-2xl mx-auto pt-20 px-4">
        <h1 className="text-4xl font-bold text-blue-900 mb-6 text-center">
          Flight Search Assistant
        </h1>
        
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <p className="text-gray-600 mb-6">
            This tool will search for the cheapest one-way flight from Bali to Oman on January 12, 2025 using Google Flights.
          </p>
          
          <Button
            onClick={handleSearch}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Searching Flights...
              </>
            ) : (
              "Search Flights"
            )}
          </Button>
        </div>

        {result && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-blue-900 mb-4">Search Results</h2>
            <p className="text-gray-600 whitespace-pre-wrap">{result}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Index;