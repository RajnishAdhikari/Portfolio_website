import React from 'react';
import { Award, Calendar, ExternalLink } from 'lucide-react';
import { resolveMediaUrl } from '@/lib/media';

const CertificationsSection = ({ certifications }) => {
    if (!certifications || certifications.length === 0) return null;

    return (
        <section className="py-20 px-4 bg-slate-50 dark:bg-slate-800">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-12 text-center">
                    Certifications
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {certifications.map((cert, index) => (
                        <div
                            key={cert.id}
                            className="group bg-white dark:bg-slate-900 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-slate-200 dark:border-slate-700"
                            style={{ animationDelay: `${index * 100}ms` }}
                        >
                            {/* Certificate Image */}
                            {cert.image ? (
                                <div className="relative h-40 overflow-hidden bg-gradient-to-br from-amber-400 to-orange-500">
                                    <img
                                        src={resolveMediaUrl(cert.image)}
                                        alt={cert.name}
                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                                    />
                                </div>
                            ) : (
                                <div className="h-40 bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
                                    <Award size={48} className="text-white opacity-50" />
                                </div>
                            )}

                            <div className="p-5">
                                <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2 line-clamp-2">
                                    {cert.name}
                                </h3>
                                <p className="text-sm font-semibold text-blue-600 dark:text-blue-400 mb-3">
                                    {cert.issuer}
                                </p>

                                <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400 mb-3">
                                    <Calendar size={16} />
                                    {cert.issue_month_year}
                                </div>

                                {cert.cred_id && (
                                    <p className="text-xs text-slate-500 dark:text-slate-500 mb-3 font-mono">
                                        ID: {cert.cred_id}
                                    </p>
                                )}

                                {cert.description && (
                                    <p className="text-sm text-slate-600 dark:text-slate-400 mb-4 line-clamp-2">
                                        {cert.description}
                                    </p>
                                )}

                                {cert.cred_url && (
                                    <a
                                        href={cert.cred_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                                    >
                                        <ExternalLink size={14} />
                                        Verify
                                    </a>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default CertificationsSection;
