import React from 'react';
import { BookOpen, Calendar, ExternalLink, FileText, Star } from 'lucide-react';
import { resolveMediaUrl } from '@/lib/media';

const ResourcePapersSection = ({ papers }) => {
    if (!papers || papers.length === 0) return null;

    // Show only featured or first 6 papers
    const displayPapers = papers.filter(p => p.is_featured).slice(0, 6);
    const papersToShow = displayPapers.length > 0 ? displayPapers : papers.slice(0, 6);

    return (
        <section className="py-20 px-4 bg-slate-50 dark:bg-slate-800">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-12 text-center">
                    Research & Resources
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {papersToShow.map((paper, index) => (
                        <div
                            key={paper.id}
                            className="group bg-white dark:bg-slate-900 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-slate-200 dark:border-slate-700"
                            style={{ animationDelay: `${index * 100}ms` }}
                        >
                            {/* Cover Image */}
                            {paper.cover_image ? (
                                <div className="relative h-48 overflow-hidden">
                                    <img
                                        src={resolveMediaUrl(paper.cover_image)}
                                        alt={paper.title}
                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                                    />
                                    {paper.is_featured && (
                                        <div className="absolute top-4 right-4 bg-yellow-400 text-slate-900 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                                            <Star size={14} />
                                            Featured
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <div className="h-48 bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
                                    <BookOpen size={64} className="text-white opacity-50" />
                                </div>
                            )}

                            <div className="p-6">
                                <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400 mb-3">
                                    <Calendar size={16} />
                                    {new Date(paper.created_at).toLocaleDateString('en-US', {
                                        year: 'numeric',
                                        month: 'long',
                                        day: 'numeric'
                                    })}
                                </div>

                                <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-3">
                                    {paper.title}
                                </h3>

                                <p className="text-slate-600 dark:text-slate-400 mb-6 line-clamp-3">
                                    {paper.excerpt}
                                </p>

                                <div className="flex gap-3">
                                    {paper.pdf_attachment && (
                                        <a
                                            href={resolveMediaUrl(paper.pdf_attachment)}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors text-sm font-medium"
                                        >
                                            <FileText size={16} />
                                            Download PDF
                                        </a>
                                    )}
                                    {paper.external_url && (
                                        <a
                                            href={paper.external_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                                        >
                                            <ExternalLink size={16} />
                                            View Online
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

export default ResourcePapersSection;
