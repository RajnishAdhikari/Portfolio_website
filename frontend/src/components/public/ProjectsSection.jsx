import React from 'react';
import { ExternalLink, Github, FileText } from 'lucide-react';
import { resolveMediaUrl } from '@/lib/media';

const ProjectsSection = ({ projects }) => {
    if (!projects || projects.length === 0) return null;

    return (
        <section className="py-20 px-4 bg-slate-50 dark:bg-slate-800">
            <div className="max-w-6xl mx-auto">
                <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-12 text-center">
                    Featured Projects
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {projects.map((project, index) => (
                        <div
                            key={project.id}
                            className="group bg-white dark:bg-slate-900 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-slate-200 dark:border-slate-700 flex flex-col"
                            style={{ animationDelay: `${index * 100}ms` }}
                        >
                            {/* Project Image */}
                            {project.cover_image ? (
                                <div className="relative h-48 overflow-hidden bg-gradient-to-br from-blue-500 to-indigo-600">
                                    <img
                                        src={resolveMediaUrl(project.cover_image)}
                                        alt={project.title}
                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                                    />
                                </div>
                            ) : (
                                <div className="h-48 bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
                                    <span className="text-6xl font-bold text-white opacity-50">
                                        {project.title?.charAt(0) || 'P'}
                                    </span>
                                </div>
                            )}

                            {/* Content */}
                            <div className="p-6 flex-1 flex flex-col">
                                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
                                    {project.title}
                                </h3>
                                <p className="text-slate-600 dark:text-slate-400 mb-4 line-clamp-3 flex-1">
                                    {project.short_desc}
                                </p>

                                {/* Tech Stack */}
                                {project.tech_stack && project.tech_stack.length > 0 && (
                                    <div className="flex flex-wrap gap-2 mb-4">
                                        {project.tech_stack.slice(0, 3).map((tech, i) => (
                                            <span
                                                key={i}
                                                className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 text-xs rounded-lg font-medium"
                                            >
                                                {tech}
                                            </span>
                                        ))}
                                        {project.tech_stack.length > 3 && (
                                            <span className="px-2 py-1 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 text-xs rounded-lg font-medium">
                                                +{project.tech_stack.length - 3}
                                            </span>
                                        )}
                                    </div>
                                )}

                                {/* Links */}
                                <div className="flex gap-3 mt-auto">
                                    {project.github_url && (
                                        <a
                                            href={project.github_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center gap-2 px-4 py-2 bg-slate-900 dark:bg-slate-700 text-white rounded-lg hover:bg-slate-800 dark:hover:bg-slate-600 transition-colors text-sm"
                                        >
                                            <Github size={16} />
                                            Code
                                        </a>
                                    )}
                                    {project.external_url && (
                                        <a
                                            href={project.external_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                                        >
                                            <ExternalLink size={16} />
                                            Live
                                        </a>
                                    )}
                                    {project.pdf_attachment && (
                                        <a
                                            href={resolveMediaUrl(project.pdf_attachment)}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
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

export default ProjectsSection;
