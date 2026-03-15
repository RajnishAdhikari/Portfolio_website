import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Calendar, ArrowLeft, ExternalLink, FileText } from 'lucide-react';

import publicApi from '@/services/publicApi';
import { resolveMediaUrl } from '@/lib/media';

const BlogPost = () => {
    const { slug } = useParams();

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [article, setArticle] = useState(null);

    useEffect(() => {
        let isMounted = true;

        const loadArticle = async () => {
            try {
                setLoading(true);
                setError('');
                const response = await publicApi.getArticleBySlug(slug);
                if (isMounted) {
                    setArticle(response.data || null);
                }
            } catch (err) {
                if (isMounted) {
                    setError('Article not found or failed to load.');
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        };

        loadArticle();
        return () => {
            isMounted = false;
        };
    }, [slug]);

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
                <p className="text-slate-600 dark:text-slate-300">Loading article...</p>
            </div>
        );
    }

    if (error || !article) {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center px-4">
                <div className="text-center">
                    <p className="text-slate-700 dark:text-slate-300 mb-4">{error || 'Article not found.'}</p>
                    <Link to="/" className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                        <ArrowLeft size={16} /> Back Home
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <article className="min-h-screen bg-slate-50 dark:bg-slate-900 py-10 px-4">
            <div className="max-w-3xl mx-auto">
                <Link to="/" className="inline-flex items-center gap-2 text-blue-600 dark:text-blue-400 mb-6 hover:underline">
                    <ArrowLeft size={16} /> Back Home
                </Link>

                {article.cover_image && (
                    <img
                        src={resolveMediaUrl(article.cover_image)}
                        alt={article.title}
                        className="w-full h-64 md:h-80 object-cover rounded-xl mb-6"
                    />
                )}

                <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-3">{article.title}</h1>
                <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400 mb-6">
                    <Calendar size={16} />
                    <span>{new Date(article.created_at).toLocaleDateString()}</span>
                </div>

                {article.excerpt && (
                    <p className="text-lg text-slate-700 dark:text-slate-300 mb-6">{article.excerpt}</p>
                )}

                {article.body ? (
                    <div
                        className="prose prose-slate dark:prose-invert max-w-none"
                        dangerouslySetInnerHTML={{ __html: article.body }}
                    />
                ) : null}

                <div className="flex gap-3 mt-8">
                    {article.external_url && (
                        <a
                            href={article.external_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                        >
                            <ExternalLink size={16} />
                            External
                        </a>
                    )}
                    {article.pdf_attachment && (
                        <a
                            href={resolveMediaUrl(article.pdf_attachment)}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-2 px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-800"
                        >
                            <FileText size={16} />
                            PDF
                        </a>
                    )}
                </div>
            </div>
        </article>
    );
};

export default BlogPost;
