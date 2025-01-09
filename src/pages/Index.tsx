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
      // Open Streamlit app in a new window
      window.open("http://localhost:8501", "_blank");
      toast({
        title: "Streamlit App Opened",
        description: "The flight search application has been opened in a new window.",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please make sure the Streamlit app is running. Run 'streamlit run src/utils/flightSearch.py' in your terminal.",
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
            Click the button below to open the Streamlit flight search application. Make sure you have started the Streamlit server first by running:<br/>
            <code className="bg-gray-100 px-2 py-1 rounded">streamlit run src/utils/flightSearch.py</code>
          </p>
          
          <Button
            onClick={handleSearch}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Opening Streamlit App...
              </>
            ) : (
              "Open Flight Search"
            )}
          </Button>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold text-blue-900 mb-4">Setup Instructions</h2>
          <ol className="list-decimal list-inside space-y-2 text-gray-600">
            <li>Install Python 3.8 or higher</li>
            <li>Install required dependencies: <code className="bg-gray-100 px-2 py-1 rounded">pip install -r requirements.txt</code></li>
            <li>Install Playwright: <code className="bg-gray-100 px-2 py-1 rounded">playwright install</code></li>
            <li>Set your OpenAI API key in environment variables</li>
            <li>Run the Streamlit app: <code className="bg-gray-100 px-2 py-1 rounded">streamlit run src/utils/flightSearch.py</code></li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default Index;