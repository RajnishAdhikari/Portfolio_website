import React from 'react';
import { Sparkles, Calendar, ExternalLink } from 'lucide-react';
import { resolveMediaUrl } from '@/lib/media';

const ExtracurricularSection = ({ activities }) => {
    if (!activities || activities.length === 0) return null;

    return (
        <section className="py-20 px-4 bg-white dark:bg-slate-900">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-12 text-center">
                    Extracurricular Activities
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {activities.map((activity, index) => (
                        <div
                            key={activity.id}
                            className="group bg-gradient-to-br from-slate-50 to-purple-50 dark:from-slate-800 dark:to-slate-900 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-slate-200 dark:border-slate-700"
                            style={{ animationDelay: `${index * 100}ms` }}
                        >
                            <div className="flex gap-4">
                                {activity.certificate_image && (
                                    <div className="flex-shrink-0">
                                        <img
                                            src={resolveMediaUrl(activity.certificate_image)}
                                            alt={activity.title}
                                            className="w-24 h-24 rounded-lg object-cover border-2 border-slate-200 dark:border-slate-700"
                                        />
                                    </div>
                                )}

                                <div className="flex-1">
                                    <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
                                        {activity.title}
                                    </h3>

                                    {activity.organisation && (
                                        <p className="text-sm font-semibold text-purple-600 dark:text-purple-400 mb-2">
                                            {activity.organisation}
                                        </p>
                                    )}

                                    {(activity.start_month_year || activity.end_month_year) && (
                                        <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400 mb-3">
                                            <Calendar size={14} />
                                            {activity.start_month_year} {activity.end_month_year && `- ${activity.end_month_year}`}
                                        </div>
                                    )}

                                    {activity.description && (
                                        <p className="text-sm text-slate-600 dark:text-slate-400 mb-3 line-clamp-3">
                                            {activity.description}
                                        </p>
                                    )}

                                    {activity.external_url && (
                                        <a
                                            href={activity.external_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="inline-flex items-center gap-2 px-3 py-1.5 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm"
                                        >
                                            <ExternalLink size={14} />
                                            Learn More
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

export default ExtracurricularSection;
