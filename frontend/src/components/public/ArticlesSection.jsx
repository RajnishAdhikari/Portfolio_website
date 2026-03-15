import React from 'react';
import { Link } from 'react-router-dom';
import { Calendar, ExternalLink, FileText, Star } from 'lucide-react';
import { resolveMediaUrl } from '@/lib/media';

const ArticlesSection = ({ articles }) => {
    if (!articles || articles.length === 0) return null;

    // Show only featured or first 6 articles
    const displayArticles = articles.filter(a => a.is_featured).slice(0, 6);
    const articlesToShow = displayArticles.length > 0 ? displayArticles : articles.slice(0, 6);

    return (
        <section className="py-20 px-4 bg-white dark:bg-slate-900">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-12 text-center">
                    Articles & Blog
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {articlesToShow.map((article, index) => (
                        <div
                            key={article.id}
                            className="group bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-800 dark:to-slate-900 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-slate-200 dark:border-slate-700"
                            style={{ animationDelay: `${index * 100}ms` }}
                        >
                            {/* Cover Image */}
                            {article.cover_image && (
                                <div className="relative h-48 overflow-hidden">
                                    <img
                                        src={resolveMediaUrl(article.cover_image)}
                                        alt={article.title}
                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                                    />
                                    {article.is_featured && (
                                        <div className="absolute top-4 right-4 bg-yellow-400 text-slate-900 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                                            <Star size={14} />
                                            Featured
                                        </div>
                                    )}
                                </div>
                            )}

                            <div className="p-6">
                                <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400 mb-3">
                                    <Calendar size={16} />
                                    {new Date(article.created_at).toLocaleDateString('en-US', {
                                        year: 'numeric',
                                        month: 'long',
                                        day: 'numeric'
                                    })}
                                </div>

                                <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-3">
                                    {article.title}
                                </h3>

                                <p className="text-slate-600 dark:text-slate-400 mb-6 line-clamp-3">
                                    {article.excerpt}
                                </p>

                                <div className="flex gap-3">
                                    {article.slug && (
                                        <Link
                                            to={`/blog/${article.slug}`}
                                            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium"
                                        >
                                            Open Post
                                        </Link>
                                    )}
                                    {article.external_url && (
                                        <a
                                            href={article.external_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                                        >
                                            <ExternalLink size={16} />
                                            Read More
                                        </a>
                                    )}
                                    {article.pdf_attachment && (
                                        <a
                                            href={resolveMediaUrl(article.pdf_attachment)}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center gap-2 px-4 py-2 bg-slate-700 dark:bg-slate-600 text-white rounded-lg hover:bg-slate-800 dark:hover:bg-slate-500 transition-colors text-sm font-medium"
                                        >
                                            <FileText size={16} />
                                            PDF
                                        </a>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default ArticlesSection;
