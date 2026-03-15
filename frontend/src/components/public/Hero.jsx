import React from 'react';
import { Mail, MapPin, Github, Linkedin, Twitter, Download } from 'lucide-react';
import { resolveMediaUrl } from '@/lib/media';

const Hero = ({ personalInfo }) => {
    if (!personalInfo) return null;

    const { full_name, tagline, email, phone, address, github_url, linkedin_url, twitter_url, profile_pic, cv_file } = personalInfo;

    return (
        <section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 px-4 py-20">
            <div className="max-w-6xl mx-auto">
                <div className="flex flex-col md:flex-row items-center gap-12">
                    {/* Profile Image */}
                    <div className="flex-shrink-0">
                        <div className="relative group">
                            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition duration-300"></div>
                            <div className="relative">
                                {profile_pic ? (
                                    <img
                                        src={resolveMediaUrl(profile_pic)}
                                        alt={full_name}
                                        className="max-w-sm w-auto h-auto rounded-xl object-contain border-4 border-white dark:border-slate-800 shadow-2xl"
                                    />
                                ) : (
                                    <div className="w-64 h-64 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center border-4 border-white dark:border-slate-800 shadow-2xl">
                                        <span className="text-7xl font-bold text-white">
                                            {full_name?.charAt(0) || 'U'}
                                        </span>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Content */}
                    <div className="flex-1 text-center md:text-left">
                        <h1 className="text-5xl md:text-6xl font-bold text-slate-900 dark:text-white mb-4 animate-fade-in">
                            {full_name}
                        </h1>
                        {tagline && (
                            <p className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-8 animate-fade-in-delay">
                                {tagline}
                            </p>
                        )}

                        {/* Download CV Button */}
                        {cv_file && (
                            <div className="mb-8">
                                <a
                                    href={resolveMediaUrl(cv_file)}
                                    download
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="inline-flex items-center gap-3 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 font-semibold"
                                >
                                    <Download size={20} />
                                    <span>Download CV</span>
                                </a>
                            </div>
                        )}

                        {/* Contact Info */}
                        <div className="flex flex-wrap gap-4 mb-8 justify-center md:justify-start">
                            {email && (
                                <a
                                    href={`mailto:${email}`}
                                    className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400"
                                >
                                    <Mail size={18} />
                                    <span className="text-sm">{email}</span>
                                </a>
                            )}
                            {address && (
                                <div className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-800 rounded-lg shadow-md text-slate-700 dark:text-slate-300">
                                    <MapPin size={18} />
                                    <span className="text-sm">{address}</span>
                                </div>
                            )}
                        </div>

                        {/* Social Links */}
                        <div className="flex gap-4 justify-center md:justify-start">
                            {github_url && (
                                <a
                                    href={github_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="p-3 bg-white dark:bg-slate-800 rounded-full shadow-md hover:shadow-lg transition-all duration-300 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 hover:scale-110"
                                >
                                    <Github size={24} />
                                </a>
                            )}
                            {linkedin_url && (
                                <a
                                    href={linkedin_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="p-3 bg-white dark:bg-slate-800 rounded-full shadow-md hover:shadow-lg transition-all duration-300 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 hover:scale-110"
                                >
                                    <Linkedin size={24} />
                                </a>
                            )}
                            {twitter_url && (
                                <a
                                    href={twitter_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="p-3 bg-white dark:bg-slate-800 rounded-full shadow-md hover:shadow-lg transition-all duration-300 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 hover:scale-110"
                                >
                                    <Twitter size={24} />
                                </a>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Hero;
