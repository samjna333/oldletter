<?php
/**
 * Plugin Name: 부고란 코어
 * Description: 부고란(사라지는 것들의 소식) 전용 기능. 기자 분류, 본문 강조 장치 CSS, 발행일 띠, 댓글 닫기, 메타 필드.
 * Version: 1.0.0
 * Author: 부고란 편집국
 * Text Domain: bugoran-core
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'BUGORAN_CORE_VER', '1.0.0' );
define( 'BUGORAN_LAUNCH', '2026-11-07' ); // 창간 준비호 날짜. 호수 계산 기준

/* 1. 기자 분류 (reporter) — 로그인 계정 없이 이름만 있는 기자 */
add_action( 'init', function () {
	register_taxonomy( 'reporter', array( 'post' ), array(
		'labels'            => array(
			'name'          => '기자',
			'singular_name' => '기자',
			'menu_name'     => '기자',
			'all_items'     => '모든 기자',
			'edit_item'     => '기자 편집',
			'add_new_item'  => '새 기자 추가',
		),
		'public'            => true,
		'hierarchical'      => false,
		'show_ui'           => true,
		'show_admin_column' => true,
		'show_in_rest'      => true,
		'rest_base'         => 'reporter',
		'rewrite'           => array( 'slug' => 'reporter', 'with_front' => false ),
	) );

	/* 2. 글 메타 필드 (REST 노출) */
	$fields = array(
		'seed'           => '씨앗 한 줄',
		'seed_url'       => '씨앗 출처 URL',
		'editor_note'    => '편집장 주석',
		'editor_request' => '재작성 지시',
		'corner'         => '코너 번호',
	);
	foreach ( $fields as $key => $desc ) {
		register_post_meta( 'post', $key, array(
			'type'              => 'string',
			'description'       => $desc,
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback'     => function () { return current_user_can( 'edit_posts' ); },
		) );
	}
} );

/* 3. 글쓴이 표시를 기자 이름으로 */
function bugoran_reporter_of( $post_id = null ) {
	$post_id = $post_id ? $post_id : get_the_ID();
	if ( ! $post_id ) { return null; }
	$terms = get_the_terms( $post_id, 'reporter' );
	return ( $terms && ! is_wp_error( $terms ) ) ? $terms[0] : null;
}
add_filter( 'the_author', function ( $name ) {
	if ( is_admin() ) { return $name; }
	$t = bugoran_reporter_of();
	return $t ? $t->name : $name;
} );
add_filter( 'get_the_author_display_name', function ( $name ) {
	if ( is_admin() ) { return $name; }
	$t = bugoran_reporter_of();
	return $t ? $t->name : $name;
} );
add_filter( 'author_link', function ( $link ) {
	if ( is_admin() ) { return $link; }
	$t = bugoran_reporter_of();
	if ( $t ) {
		$l = get_term_link( $t );
		if ( ! is_wp_error( $l ) ) { return $l; }
	}
	return $link;
} );

/* 4. 댓글 닫기 (답장은 편집장의 편지 지면에서) */
add_filter( 'comments_open', '__return_false', 20 );
add_filter( 'pings_open', '__return_false', 20 );
add_filter( 'comments_array', '__return_empty_array', 20 );

/* 5. 발행일 띠 단축코드 [bugoran_dateline] */
function bugoran_issue_no( $ts = null ) {
	$ts     = $ts ? $ts : current_time( 'timestamp' );
	$launch = strtotime( BUGORAN_LAUNCH . ' 00:00:00' );
	$days   = (int) floor( ( $ts - $launch ) / DAY_IN_SECONDS );
	return max( 0, $days );
}
add_shortcode( 'bugoran_dateline', function () {
	$ts   = current_time( 'timestamp' );
	$days = array( '일', '월', '화', '수', '목', '금', '토' );
	$date = wp_date( 'Y년 n월 j일', $ts ) . ' ' . $days[ (int) wp_date( 'w', $ts ) ] . '요일';
	$no   = bugoran_issue_no( $ts );
	$issue = $no === 0 ? '창간 준비호' : '제' . number_format_i18n( $no ) . '호';
	return '<div class="bg-dateline"><span>' . esc_html( $issue ) . '</span><span>' . esc_html( $date ) . '</span><span>사라지는 것들의 소식</span><span>편집 박멀미</span></div>';
} );

/* 6. 글 하단 기자 소개 */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$t = bugoran_reporter_of();
	if ( ! $t ) { return $content; }
	$desc = term_description( $t->term_id, 'reporter' );
	$box  = '<aside class="bg-reporter"><div class="bg-reporter__name"><a href="' . esc_url( get_term_link( $t ) ) . '">' . esc_html( $t->name ) . ' 기자</a></div>';
	if ( $desc ) { $box .= '<div class="bg-reporter__desc">' . wp_kses_post( $desc ) . '</div>'; }
	$box .= '<a class="bg-reporter__more" href="' . esc_url( get_term_link( $t ) ) . '">이 기자의 다른 소식</a></aside>';
	return $content . $box;
}, 20 );

/* 7. 스타일 */
add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'bugoran-core', plugins_url( 'bugoran.css', __FILE__ ), array(), BUGORAN_CORE_VER );
}, 100 );

/* 8. 검색 노출 차단 상태 표시 (정식 공개 전까지) */
add_action( 'wp_head', function () {
	if ( get_option( 'bugoran_noindex', '1' ) === '1' ) {
		echo "<meta name=\"robots\" content=\"noindex, nofollow\">\n";
	}
}, 1 );
