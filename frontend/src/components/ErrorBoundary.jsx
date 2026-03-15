import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
            errorInfo: null,
        };
    }

    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        // Log error details to console
        console.error('ErrorBoundary caught an error:', error, errorInfo);

        this.setState({
            error: error,
            errorInfo: errorInfo,
        });
    }

    handleReload = () => {
        window.location.reload();
    };

    render() {
        if (this.state.hasError) {
            const isDevelopment = import.meta.env.DEV;

            return (
                <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 dark:from-slate-900 dark:to-red-900 flex items-center justify-center px-4">
                    <div className="max-w-2xl w-full bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-8">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="p-4 bg-red-100 dark:bg-red-900 rounded-full">
                                <AlertTriangle className="w-12 h-12 text-red-600 dark:text-red-400" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
                                    Oops! Something went wrong
                                </h1>
                                <p className="text-slate-600 dark:text-slate-400 mt-1">
                                    The application encountered an unexpected error
                                </p>
                            </div>
                        </div>

                        {isDevelopment && this.state.error && (
                            <div className="mb-6 space-y-4">
                                <div className="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg p-4">
                                    <h3 className="text-sm font-semibold text-red-900 dark:text-red-300 mb-2">
                                        Error Message:
                                    </h3>
                                    <p className="text-sm text-red-800 dark:text-red-400 font-mono">
                                        {this.state.error.toString()}
                                    </p>
                                </div>

                                {this.state.errorInfo && (
                                    <div className="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg p-4">
                                        <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-300 mb-2">
                                            Component Stack:
                                        </h3>
                                        <pre className="text-xs text-slate-700 dark:text-slate-400 font-mono overflow-x-auto whitespace-pre-wrap">
                                            {this.state.errorInfo.componentStack}
                                        </pre>
                                    </div>
                                )}
                            </div>
                        )}

                        <div className="flex gap-4">
                            <button
                                onClick={this.handleReload}
                                className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
                            >
                                <RefreshCw className="w-5 h-5" />
                                Reload Page
                            </button>
                            <a
                                href="/"
                                className="flex items-center gap-2 px-6 py-3 bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-900 dark:text-white rounded-lg font-semibold transition-all duration-200"
                            >
                                Go Home
                            </a>
                        </div>

                        {!isDevelopment && (
                            <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg">
                                <p className="text-sm text-blue-900 dark:text-blue-300">
                                    <strong>Tip:</strong> If this issue persists, try clearing your browser cache or contact support.
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
