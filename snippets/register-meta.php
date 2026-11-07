<?php
/**
 * 부고란: 글 메타 필드 등록 (REST API 노출)
 * 자식 테마 functions.php 끝에 붙여 넣거나 require 한다.
 * seed: 씨앗 한 줄 / seed_url: 출처 / editor_note: 편집장 주석 / editor_request: 재작성 지시 / corner: 코너 번호
 */
add_action( 'init', function () {
    $fields = [
        'seed'           => '씨앗 한 줄',
        'seed_url'       => '씨앗 출처 URL',
        'editor_note'    => '편집장 주석',
        'editor_request' => '재작성 지시',
        'corner'         => '코너 번호',
    ];
    foreach ( $fields as $key => $desc ) {
        register_post_meta( 'post', $key, [
            'type'          => 'string',
            'description'   => $desc,
            'single'        => true,
            'show_in_rest'  => true,
            'sanitize_callback' => 'sanitize_text_field',
            'auth_callback'  => function () { return current_user_can( 'edit_posts' ); },
        ] );
    }
} );
