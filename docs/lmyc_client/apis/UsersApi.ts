/* tslint:disable */
/* eslint-disable */
/**
 * Lubricentro M&C
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * Contact: matiasadrianpp4@gmail.com
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import {
    User,
    UserFromJSON,
    UserToJSON,
} from '../models';

export interface AccountLoginPostRequest {
    body: User;
}

export interface AccountSignupPostRequest {
    body: User;
}

/**
 * 
 */
export class UsersApi extends runtime.BaseAPI {

    /**
     * Log in
     */
    async accountLoginPostRaw(requestParameters: AccountLoginPostRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<void>> {
        if (requestParameters.body === null || requestParameters.body === undefined) {
            throw new runtime.RequiredError('body','Required parameter requestParameters.body was null or undefined when calling accountLoginPost.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/account/login`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: UserToJSON(requestParameters.body),
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Log in
     */
    async accountLoginPost(requestParameters: AccountLoginPostRequest, initOverrides?: RequestInit): Promise<void> {
        await this.accountLoginPostRaw(requestParameters, initOverrides);
    }

    /**
     * Log out
     */
    async accountLogoutPostRaw(initOverrides?: RequestInit): Promise<runtime.ApiResponse<void>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/account/logout`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Log out
     */
    async accountLogoutPost(initOverrides?: RequestInit): Promise<void> {
        await this.accountLogoutPostRaw(initOverrides);
    }

    /**
     * Create new user
     */
    async accountSignupPostRaw(requestParameters: AccountSignupPostRequest, initOverrides?: RequestInit): Promise<runtime.ApiResponse<void>> {
        if (requestParameters.body === null || requestParameters.body === undefined) {
            throw new runtime.RequiredError('body','Required parameter requestParameters.body was null or undefined when calling accountSignupPost.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/account/signup`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: UserToJSON(requestParameters.body),
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Create new user
     */
    async accountSignupPost(requestParameters: AccountSignupPostRequest, initOverrides?: RequestInit): Promise<void> {
        await this.accountSignupPostRaw(requestParameters, initOverrides);
    }

}
