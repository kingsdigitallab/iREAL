export type Node = {
	_node_content: string;
	_node_type: string;
	doc_id: string;
	document_id: string;
	document_title: string;
	diseases?: string[];
	events?: string[];
	excerpt_keywords: string;
	file: string;
	geo?: GeoData;
	locations?: string[];
	media?: string[];
	next_section_summary?: string;
	organizations?: string[];
	persons?: string[];
	prev_section_summary?: string;
	questions_this_excerpt_can_answer: string;
	ref_doc_id: string;
	school: string;
	section_summary: string;
	times?: string[];
	topics: string[];
};

type GeoData = {
	geo: {
		[placeName: string]: [number, number];
	};
};

export type Result = {
	nodes: Node[];
	schoolsNames: string[];
	excerpt_keywords: Facet[];
	organizations: Facet[];
	persons: Facet[];
	locations: Facet[];
	topics: Facet[];
	years: number[];
};

export type School = {
	name: string;
	slug: string;
	excerpt_keywords: Facet[];
	topics: Facet[];
	diseases: Facet[];
	locations: Facet[];
	organizations: Facet[];
	persons: Facet[];
	years: number[];
};

export type Facet = {
	name: string;
	count: number;
	schools?: string[];
	coords?: [number, number];
};
