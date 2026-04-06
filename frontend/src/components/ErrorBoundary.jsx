import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log the error to console and state
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    this.setState({
      error: error,
      errorInfo: errorInfo
    });

    // You can also log the error to an error reporting service here
    // logErrorToService(error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      // Custom error UI
      return (
        <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
          <div className="max-w-2xl w-full bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl p-8">
            <div className="text-center">
              <div className="mx-auto w-16 h-16 bg-red-500/15 rounded-full flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              
              <h1 className="text-2xl font-bold text-slate-100 mb-4">
                Something went wrong
              </h1>
              
              <p className="text-slate-400 mb-6 leading-relaxed">
                An unexpected error occurred while loading the application. 
                This could be due to a network issue, invalid data, or a temporary system problem.
              </p>

              {/* Error details for development */}
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <details className="text-left bg-slate-800 rounded-lg p-4 mb-6">
                  <summary className="cursor-pointer text-slate-300 font-medium mb-2">
                    Technical Details
                  </summary>
                  <div className="mt-3 space-y-3">
                    <div>
                      <strong className="text-slate-400">Error:</strong>
                      <pre className="text-red-400 text-sm mt-1 overflow-x-auto">
                        {this.state.error.toString()}
                      </pre>
                    </div>
                    {this.state.errorInfo && (
                      <div>
                        <strong className="text-slate-400">Component Stack:</strong>
                        <pre className="text-amber-400 text-sm mt-1 overflow-x-auto whitespace-pre-wrap">
                          {this.state.errorInfo.componentStack}
                        </pre>
                      </div>
                    )}
                  </div>
                </details>
              )}

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button
                  onClick={this.handleReset}
                  className="inline-flex items-center justify-center rounded-2xl bg-sky-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-sky-500/20 transition hover:bg-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-300"
                >
                  Try Again
                </button>
                
                <button
                  onClick={() => window.location.reload()}
                  className="inline-flex items-center justify-center rounded-2xl bg-slate-700 px-6 py-3 text-sm font-semibold text-slate-200 shadow-lg transition hover:bg-slate-600 focus:outline-none focus:ring-2 focus:ring-slate-500"
                >
                  Refresh Page
                </button>
              </div>

              <div className="mt-8 p-4 bg-slate-800/50 rounded-lg">
                <p className="text-xs text-slate-500">
                  If this problem persists, please contact the system administrator with the error details shown above.
                </p>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
